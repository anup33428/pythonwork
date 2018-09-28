from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

# function to initialize the web driver and read the form data
def _main():
    data_file = open('data_sign_in.json', 'r')
    sign_in_data = json.load(data_file)
    data_file.close()
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("")
    _fill_sign_in_form(sign_in_data["formData"])
    # driver.close()


# function to fil the sign in form on UI
def _fill_sign_in_form(form_data):
    #assert "Python" in driver.title
    sign_in_link = driver.find_element_by_class_name("home-sign-in-link")
    sign_in_link.click()
    username_input = driver.find_element_by_id("UserName")
    password_input = driver.find_element_by_id("Password")
    username_input.clear()
    password_input.clear()
    username_input.send_keys(form_data["username"])
    password_input.send_keys(form_data["password"])
    password_input.send_keys(Keys.RETURN)

_main()
