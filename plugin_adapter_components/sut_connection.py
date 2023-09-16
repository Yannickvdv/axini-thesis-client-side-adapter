from datetime import datetime
import threading
import time
from splinter import Browser
from xmldiff import main
from lxml import etree
from io import StringIO 

props = ['style']

f = open("test.txt", "w")

class SeleniumInterface:
    """
    Constructor
    """
    def __init__(self, logger, event_queue, response_received):
        self.logger = logger
        self.event_queue = event_queue
        self.response_received = response_received
        self.driver = None
        self.page_source = ''
        self.page_url = ''


    """
    Special function: class name
    """
    def __name__(self):
        return "Sut"


    """
    Connects to the SUT and prepares it for testing.
    """
    def start(self):
        self.driver = Browser('chrome')
        self.driver.wait_time = 10
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


    """
    Perform any cleanup if the selenium has stopped
    """
    def stop(self):
        if self.driver:
            self.driver.quit()
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
        self.driver.find_by_css(css_selector).is_visible()
        self.driver.find_by_css(css_selector).click()


    """
    Navigates to the specified URL and generates a response.
    param [String] url
    """
    def open_url(self, url):
        self.driver.visit(url)


    """
    Enters the provided value into an input field
    specified by the CSS selector.
    param [String] css_selector
    param [String] value
    """
    def fill_in(self, css_selector, value):
        self.driver.find_by_css(css_selector).fill(value)


    """
    Generates a response containing the current page's title and URL.
    """
    def generate_response(self):
        # Get initial page url
        self.page_url = self.driver.url
        # Get initial page source
        self.page_source = self.driver.html
        response = [
            "page_title",
            {"title": "string", "url": "string"},
            {"title": self.driver.title, "url": self.driver.url}
        ]
        self.handle_response(response)
        return


    """
    Compares the page source before and after an action, 
    detects updates, and generates a response.
    """
    def get_updates(self):
        # if the driver is instantiated, the url is not selenium's default, and the page url has changed 
        # then dont compare differences but do a route change event instead
        if self.driver.url != "" and self.driver.url != "data:," and self.page_url != self.driver.url:
            self.generate_response()
            return
        
        # Get the current version of the UI
        current = self.driver.html
            
        # If the current is empty or same as before throw it away
        if current == "" or self.page_source == "" or current == self.page_source:
            return
        
        previous = self.page_source
        self.page_source = current

        # f1 = open("previous", "a")
        # f1.write("previous: \n")
        # f1.write(previous)
        # f1.write("\n")

        # f2 = open("current", "a")
        # f2.write("current: \n")
        # f2.write(current)
        # f2.write("\n")

        # Create a new thread and start it
        thread = threading.Thread(target=self.compare_dom_changes, args=(previous, current, threading.current_thread()))
        thread.start()


    def compare_dom_changes(self, previous, current, thread_obj):
        parser = etree.HTMLParser()

        previous = etree.parse(StringIO(previous), parser)
        current = etree.parse(StringIO(current), parser)

        results = main.diff_trees(previous, current)

        nodes = {}
        for result in results:
            attributes = {}
            fields = result._fields
            for field in fields:
                attributes[field] = str(getattr(result, field))

            if type(result).__name__ not in ['MoveNode', 'RenameNode']:
                if type(result).__name__ in nodes:
                    nodes[type(result).__name__].append(attributes)
                else:
                    nodes[type(result).__name__] = [attributes]

        if nodes:
            response = ["page_update", {'nodes': 'struct'},{'nodes': nodes}]
            self.handle_response(response)
        
        thread_obj.join()