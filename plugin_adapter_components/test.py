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
sut.browser.visit('http://localhost:3000')

time.sleep(2)

while True:
    sut.page_source = sut.browser.html
    print("do it now")
    time.sleep(5)
    sut.get_updates()
    time.sleep(1)
