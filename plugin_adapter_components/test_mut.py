import time
from logger import Logger

from sut_connection import SeleniumInterface

logger = Logger()
logger.log_level(4 & logger.LOG_ALL)

def responseCallBack(label, types, values):
    print("callback")
    # print(label)
    # print(types)
    # print(values)

sut = SeleniumInterface(logger, [], responseCallBack)
sut.start()
sut.browser.get('http://localhost:3000')

while True:
    time.sleep(20)
    pass

