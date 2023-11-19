import time
import json
from logger import Logger
from selenium.webdriver.common.by import By

from sut_connection import SeleniumInterface

logger = Logger()
logger.log_level(4 & logger.LOG_ALL)

def responseCallBack(label, types, values):
    # print(label)
    # print(types)
    # print(values)
    print("ruby:")
    if "mutations" in values:
        print("=================================================")
        print(python_to_ruby(str(values["mutations"])))
        print("=================================================")

def python_to_ruby(string):
    # Parse the Python string into a Python dictionary
    # python_dict = eval(string.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
    ruby_string = string.replace(': ', '=>').replace('\'', '"')

    # Serialize the Ruby hash to a string in the desired Ruby notation
    # ruby_string = str(ruby_hash).replace("'", '"').replace("None", "nil").replace("True", "true").replace("False", "false")

    return ruby_string

sut = SeleniumInterface(logger, [], responseCallBack)
sut.start()
sut.browser.get('http://localhost:3000')
while True:
    time.sleep(15)
    sut.browser.find_element(By.CSS_SELECTOR, ".modal-footer button.btn.btn-primary").click()    
    pass
