# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # create a new browser instance
# browser = webdriver.Chrome()

# # navigate to a webpage with the button
# browser.get("http://localhost:4200")

# # find the button by CSS selector and click it
# button = browser.find_element(By.CSS_SELECTOR, "#alert_btn")
# button.click()

# # close the browser
# browser.quit()


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from splinter import Browser

browser = Browser('firefox')
browser.visit('http://localhost:4200/')

element = browser.is_element_present_by_css(css_selector, text=title)

# # This method searches an element for the given properties and returns a list of all equal properties
# # AMP can then compare expected with actual based on the missing properties (those who were not equal)
# def element_has_properties(css_selector, property_values={}):
#     element = browser.driver.find_element(By.CSS_SELECTOR, css_selector)
#     actual_property_values = {}

#     for property_name, expected_value in property_values.items():
#         actual_value = element.get_property(property_name)
        

#         # If the element does not have the required properties, return an empty list
#         if actual_value == expected_value:
#             actual_property_values[property_name] = actual_value

#     return actual_property_values


# property_values = {
#     'textContent': 'Click!',
#     'value': '1'
# }

# print(element_has_properties("#alert_btn", property_values))