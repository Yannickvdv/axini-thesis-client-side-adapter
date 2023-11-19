from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import asyncio
import threading
import json
import websockets
import os

class SeleniumInterface:
    """
    Constructor
    """
    def __init__(self, logger, event_queue, response_received):
        self.logger = logger
        self.event_queue = event_queue
        self.response_received = response_received
        self.browser = None
        self.websocket_server = None
        self.websocket_thread = None
        self.coverage_folder = self.get_coverage_folder()


    """
    Special function: class name
    """
    def __name__(self):
        return "Sut"


    """
    Connects to the SUT and prepares it for testing.
    """
    def start(self):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()

        # Start the WebSocket server in a separate thread
        self.websocket_thread = threading.Thread(target=self.run_websocket_server)
        self.websocket_thread.start()
        self.websocket_thread_close_event = Event_ts()

        # Inject JavaScript code to set up a MutationObserver for every page load
        mutation_script = open('./plugin_adapter_components/mutation_observer/mutation_observer_script.js', 'r').read()
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': mutation_script})

        self.browser.wait_time = 10
        self.logger.info("Sut", "Started Selenium browser")


    """
    Prepares the SUT for a new test case.
    """
    def reset(self):
        self.logger.info("Sut", "Resetting Selenium browser started")
        self.stop()
        time.sleep(3)
        self.start()
        self.logger.info("Sut", "Resetting Selenium browser completed")


    def create_coverage(self):
        coverage_data = self.browser.execute_script('return window.__coverage__;')

        if coverage_data:
            print('test')
            json_data = json.dumps(coverage_data)
            timestamp = int(time.time())
            coverage_folder = self.coverage_folder
            file_name = f"{coverage_folder}/coverage_{timestamp}.json"
            file = open(file_name, "w")
            file.write(json_data)


    def get_coverage_folder(self):
        base_path = 'plugin_adapter_components/coverage_reports'
        # List all subdirectories in the base path
        subdirectories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

        if not subdirectories:
            # If there are no existing folders, create the first one
            new_folder_name = "1"
        else:
            # Find the highest folder number and increment it
            number_directories = [int(d) for d in subdirectories if d.isdigit()]
            max_folder_number = max(number_directories) if len(number_directories) > 0 else 0 
            # max_folder_number = max([int(d) for d in subdirectories if d.isdigit()])
            new_folder_name = str(max_folder_number + 1)

        new_folder_path = os.path.join(base_path, new_folder_name)

        # Create the new folder
        os.mkdir(new_folder_path)

        return new_folder_path

    """
    Perform any cleanup if the selenium has stopped
    """
    def stop(self):
        self.create_coverage()
        # while True:
        #     time.sleep(20)

        if self.browser:
            self.browser.quit()

        if self.websocket_thread:
            self.websocket_thread_close_event.set()
            self.websocket_server.close()
            self.websocket_thread.join()

        self.logger.info("Sut", "Stopped Selenium browser")

    """
    Parse the SUT's response and add it to the response stack from the
    Handler class.
    """
    def handle_response(self, response):
        self.logger.debug("Sut", "Add response: {}".format(response))
        self.response_received(response[0], response[1], response[2])


    """
    Simulates a click on an element specified by the 
    CSS selector
    param [String] css_selector
    """
    def click(self, css_selector):
        self.browser.find_element(By.CSS_SELECTOR, css_selector).is_displayed()
        self.browser.find_element(By.CSS_SELECTOR, css_selector).click()


    """
    Navigates to the specified URL and generates a response.
    param [String] url
    """
    def open_url(self, url):
        self.browser.get(url)
 

    """
    Refreshes the current page
    """
    def refresh(self):
        self.browser.refresh()
        time.sleep(1)

    """
    Enters the provided value into an input field
    specified by the CSS selector.
    param [String] css_selector
    param [String] value
    """
    def fill_in(self, css_selector, value):
        element = self.browser.find_element(By.CSS_SELECTOR, css_selector)
        self.browser.execute_script(f"arguments[0].setAttribute('value', '{value}');", element)
        self.browser.execute_script("var event = new Event('input', { bubbles: true }); arguments[0].dispatchEvent(event);", element)


    def accept_alert(self):
        self.browser.switch_to.alert.accept()

    def run_websocket_server(self):
        asyncio.run(self.start_websocket_server())


    async def start_websocket_server(self):
        self.websocket_server = await websockets.serve(self.handle_browser_data, "localhost", 8765)
        await asyncio.gather(self.websocket_server.wait_closed(), self.websocket_thread_close_event.wait())
        self.logger.info("Sut", "Closing websocket")


    # Define a callback to handle incoming messages from the browser
    async def handle_browser_data(self, websocket):
        async for message in websocket:
            message = json.loads(message)
            response = None
            if (message["label"] == "page_loaded"):
                response = [
                    "page_title",
                    {"title": "string", "url": "string"},
                    {"title": message["title"], "url": message["url"]}
                ]
            elif (message["label"] == "page_updated"):
                response = [
                    "page_update", 
                    {"mutations": "struct"},
                    {
                        "mutations": {
                            "characterData": message["characterData"],
                            "attributes": message["attributes"],
                            "childList": message["childList"]
                        }
                    }
                ]
            self.handle_response(response)

class Event_ts(asyncio.Event):
    #TODO: clear() method
    def set(self):
        #FIXME: The _loop attribute is not documented as public api!
        self._loop.call_soon_threadsafe(super().set)