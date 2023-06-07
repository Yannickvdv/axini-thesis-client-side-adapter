import time
from splinter import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import difflib

class SeleniumInterface:
    """
    Constructor
    """
    def __init__(self, logger, responses, event_queue, response_received):
        self.logger = logger
        self.responses = responses
        self.event_queue = event_queue
        self.response_received = response_received
        self.browser = None
        self.page_source = ''

    """
    Special function: class name
    """
    def __name__(self):
        return "Sut"

    """
    Connects to the SUT and prepares it for testing.
    """
    def start(self):
        self.browser = Browser('firefox')
        self.logger.info("Sut", "Started Selenium browser")

    """
    Prepares the SUT for a new test case.
    """
    def reset(self):
        self.logger.info("Sut", "Resetting Selenium browser started")
        self.stop()
        self.start()
        self.logger.info("Sut", "Resetting Selenium browser completed")

    """
    Perform any cleanup if the selenium has stopped
    """
    def stop(self):
        if self.browser:
            self.browser.quit()
        self.logger.info("Sut", "Stopped Selenium browser")

    """
    Parse the SUT's response and add it to the response stack from the
    Handler class.
    """
    def handle_response(self, response):
        self.logger.debug("Sut", "Add response: {}".format(response))
        self.response_received(response[0], response[1], response[2])


    def click(self, css_selector):
        self.page_source = self.browser.html
        self.browser.find_by_css(css_selector).first.click()
        time.sleep(3)


    def click_link(self, css_selector):
        self.browser.find_by_css(css_selector).first.click()
        time.sleep(2)
        self.generate_response()


    def visit(self, url):
        self.browser.visit(url)
        self.generate_response()


    def fill_in(self, css_selector, value):
        self.page_source = self.browser.html
        self.browser.find_by_css(css_selector).fill(value)


    # Create a new Browser instance
    def start(self, headless=True):
        self.browser = Browser('chrome', headless=headless)
        self.browser.wait_time = 5
        #WebDriverWait(self.browser.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body.loaded')))


    def generate_response(self):

        self.page_source = self.browser.html
        response = [
            "page_title",
            {"_title": "string", "_url": "string"},
            {"_title": self.browser.title, "_url": self.browser.url}
        ]
        self.handle_response(response)
        return


    def get_updates(self):

        if not self.page_source:
            return
        
        current_page_source = self.browser.html
        diff = difflib.unified_diff(self.page_source.splitlines(), current_page_source.splitlines())
        added_lines = []
        removed_lines = []

        for line in diff:
            if line.startswith('+'):
                added_lines.append(line[1:].replace('\t','').replace('\n',''))
            elif line.startswith('-'):
                removed_lines.append(line[1:].replace('\t','').replace('\n',''))

        if added_lines or removed_lines:
            print('Added lines:')
            print(added_lines)

            print('Removed lines:')
            print(removed_lines)

            response = ["page_update", {'added_lines': 'array', 'removed_lines':'array' },{'added_lines': added_lines[1:],'removed_lines':removed_lines[1:]}]
            self.handle_response(response)
        self.page_source = current_page_source
