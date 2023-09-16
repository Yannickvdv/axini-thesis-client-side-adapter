from splinter import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from logger import Logger

from sut_connection import SeleniumInterface

logger = Logger()
logger.log_level(4 & logger.LOG_ALL)

sut = SeleniumInterface(logger, [], ())
sut.start()
sut.driver.visit('http://localhost:3000')
sut.page_url = sut.driver.url
print(sut.page_url)
# sut.browser.visit('http://localhost:3000')

while True:
    time.sleep(0.01)
    sut.get_updates()
    
while True:
    input("Get source?")
    sut.page_source = sut.browser.html
    print("Got source!")
    
    input("Get update?")
    sut.get_updates()
    print("Got update!")
