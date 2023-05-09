from selenium import webdriver
from selenium.webdriver.common.by import By

# create a new browser instance
browser = webdriver.Chrome()

# navigate to a webpage with the button
browser.get("http://localhost:4200")

# find the button by CSS selector and click it
button = browser.find_element(By.CSS_SELECTOR, "#alert_btn")
button.click()

# close the browser
browser.quit()
