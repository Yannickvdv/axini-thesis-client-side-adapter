from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from splinter import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Element:
    def __init__(self, css_selector, title, value, expect):
        self.value = value
        self.title = title
        self.css_selector = css_selector
        self.expect = expect
        
class SeleniumInterface:

    """
    Constructor
    """
    def __init__(self, logger, response_received):
        self.logger = logger
        self.response_received = response_received
        self.browser = None


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
    def handle_response(self, response=None):
        self.logger.debug("Sut", "Add response: {}".format(response))
        self.response_received(response[0], response[1], response[2])


    def click(self, css_selector):
        self.browser.find_by_css(css_selector).first.click()
        time.sleep(2)


    def expect_page_to_have(self, css_selector, title=None):
        if title:
            element = self.browser.is_element_present_by_css(css_selector, text=title)
        else:
            element = self.browser.is_element_present_by_css(css_selector)

        response = ["expect_page_to_have", { "found": "string" }, {"found": element}]
        return self.handle_response(response)


    def expect_page_not_to_have(self, css_selector, title=None):
        if title:
            element = self.browser.is_element_present_by_css(css_selector, text=title)
        else:
            element = self.browser.is_element_present_by_css(css_selector)
        response = ["expect_page_not_to_have", { "not_found": "string"}, {"not_found": element}]
        return self.handle_response(response)


    def visit(self, url):
        self.browser.visit(url)
        self.get_url()


    def get_url(self):
        response = ["url_opened", {"url" : "string"}, {"url": self.browser.url}]
        print(self.browser.url)
        return self.handle_response(response)


    def get_value(self, css_selector):
        value = self.browser.find_by_css(css_selector).first.value
        response = ["get_value", { "css_selector": "string", "value": "string" }, {"css_selector": css_selector, "value": value}]
        return self.handle_response(response)


    def fill_in(self, css_selector, value):
        self.browser.find_by_css(css_selector).fill(value)
        time.sleep(2)

    def show_success(self):
        self.browser.find_by_css('.not-found-card')
        return self.handle_response()
    
    def show_success(self):
        self.browser.find_by_css('.not-found-card')
        return self.handle_response()