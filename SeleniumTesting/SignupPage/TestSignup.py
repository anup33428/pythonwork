from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import json
import random

def _main():
    data_file = open("data_apply_now.json", "r")
    apply_now_data = json.load(data_file)
    data_file.close()
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("")
    _fill_apply_now_form(apply_now_data["formData"])

def _fill_apply_now_form(form_data):
    apply_link = driver.find_element_by_class_name("btn-home-apply")
    apply_link.click()
    email_input = driver.find_element_by_id("AccountSecurity_Email")
    password_input = driver.find_element_by_id("AccountSecurity_Password")
    re_enter_password_input = driver.find_element_by_id("AccountSecurity_VerifyPassword")
    security_question_dropdown = Select(driver.find_element_by_id("AccountSecurity_SecurityQuestion"))
    security_answer_input = driver.find_element_by_id("AccountSecurity_SecurityAnswer")
    email_input.clear()
    password_input.clear()
    re_enter_password_input.clear()
    security_answer_input.clear()
    email_input.send_keys(form_data["email"])
    password_input.send_keys(form_data["password"])
    re_enter_password_input.send_keys(form_data["reenterpassword"])
    security_question_dropdown.select_by_index(random.randint(1,6))
    security_answer_input.send_keys(form_data["securityanswer"])
    security_answer_input.send_keys(Keys.RETURN)


_main()
