from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import random
import sys
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-b", action='store', default='chrome', dest='browser', help='Browser name, ex chrome, firefox, edge, etc. Default value is chrome')
parser.add_argument("-i", action='store', default=1, dest='iteration', type=int, help='Number of iteration the script runs. Default value is 1')
results = parser.parse_args()
index = 1



def _main():
    data_file = open("data_loan_application.json", "r")
    loan_application_data = json.load(data_file)
    data_file.close()
    global driver
    if results.browser == 'chrome':
        driver = webdriver.Chrome()
    elif results.browser == 'firefox':
        driver = webdriver.Firefox()
    elif results.browser == 'edge':
        driver = webdriver.Edge()
    else:
        print("Invaild Browser Name.")
        exit()

    driver.maximize_window()
    driver.get("siteurl")
    if loan_application_data["testsignup"]:
        data_file = open("data_apply_now.json", "r")
        signup_data = json.load(data_file)
        data_file.close()
        _fill_apply_now_form(signup_data["formData"])
    else:
        data_file = open("data_sign_in.json", "r")
        signin_data = json.load(data_file)
        data_file.close()
        sign_in = _fill_sign_in_form(signin_data["formData"])
        time.sleep(5)
        continuebtn = driver.find_element_by_xpath("//a[@href='siteurl/path']") #css_selector('.btn.btn-apply.btn-lg.btn-block')
        continuebtn.click()


    _fill_loan_application(loan_application_data["formData"])
    time.sleep(5)
    income_form = _fill_income_details(loan_application_data["formData"]["incomeInfo"])
    time.sleep(5)
    _review_income_details()
    time.sleep(5)
    _fill_bank_details(loan_application_data["formData"]["bankInfo"])
    time.sleep(5)
    driver.close()


def _fill_loan_application(form_data):
    personal_info = form_data["personalInfo"]
    try:
        page_loaded =  WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "FirstName")))
    except:
        print("Response timed out")
    first_name = driver.find_element_by_id("FirstName")
    first_name.clear()
    first_name.send_keys(personal_info["firstName"])
    middle_name = driver.find_element_by_id("MiddleInitial")
    middle_name.clear()
    middle_name.send_keys(personal_info["middleName"])
    last_name = driver.find_element_by_id("LastName")
    last_name.clear()
    last_name.send_keys(personal_info["lastName"])
    Select(driver.find_element_by_id("BirthDate_Month")).select_by_index(random.randint(1,12))
    Select(driver.find_element_by_id("BirthDate_Day")).select_by_index(random.randint(1,28))
    Select(driver.find_element_by_id("BirthDate_Year")).select_by_index(random.randint(15,90))
    driver.find_element_by_id("NIN").clear()
    driver.find_element_by_id("NIN").send_keys(personal_info["ssn"])
    Select(driver.find_element_by_id("Identification_TypeKey")).select_by_visible_text(personal_info["idType"])

    contact_info = form_data["contactInfo"]
    driver.find_element_by_id("Address_Address").clear()
    driver.find_element_by_id("Address_Address").send_keys(contact_info["streetAddress"])
    Select(driver.find_element_by_id("Address_UnitType")).select_by_visible_text(contact_info["houseType"])
    driver.find_element_by_id("Address_UnitNumber").clear()
    driver.find_element_by_id("Address_UnitNumber").send_keys(contact_info["houseNumber"])
    driver.find_element_by_id("Address_City").clear()
    driver.find_element_by_id("Address_City").send_keys(contact_info["city"])
    Select(driver.find_element_by_id("Address_State")).select_by_visible_text(contact_info["state"])
    driver.find_element_by_id("Address_Zip").clear()
    driver.find_element_by_id("Address_Zip").send_keys(contact_info["zipcode"])
    Select(driver.find_element_by_id("ResidenceSince_Month")).select_by_index(random.randint(1,12))
    Select(driver.find_element_by_id("ResidenceSince_Year")).select_by_index(random.randint(2,90))
    driver.find_element_by_id("PrimaryPhone").clear()
    driver.find_element_by_id("PrimaryPhone").send_keys(contact_info["homePhone"])
    driver.find_element_by_id("SecondaryPhone").clear()
    driver.find_element_by_id("SecondaryPhone").send_keys(contact_info["mobilePhone"])
    driver.find_element_by_css_selector(".custom-control.custom-radio.mbxl").click()
    #driver.find_element_by_xpath("//*[@id='IsMilitary']/input[1]")
    driver.find_element_by_id("Identification_Number").clear()
    driver.find_element_by_id("Identification_Number").send_keys(personal_info["idNumber"])
    Select(driver.find_element_by_id("Identification_State")).select_by_visible_text(personal_info["idState"])
    #driver.find_element_by_id("CommunicationConsentPromotional").send_keys(contact_info["promotions"])
    #driver.find_element_by_id("CommunicationConsentOperational").send_keys(contact_info["accAlert"])
    driver.find_element_by_id("btnNext").click()


def _fill_income_details(income_data):
    try:
        page_loaded =  WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "EditableIncome_IncomeTypeCode")))
    except:
        print("Response timed out")
    income_type =Select(driver.find_element_by_id("EditableIncome_IncomeTypeCode"))
    income_type.select_by_index(random.choice([1,2,4,5]))
    #income_type.select_by_visible_text("Employed")
    selected_input_type= income_type.first_selected_option.text
    if selected_input_type == "Employed":
        emp_name = driver.find_element_by_id("EditableIncome_Employer")
        emp_name.clear()
        emp_name.send_keys(income_data["employer"])
        work_phone = driver.find_element_by_id("EditableIncome_WorkPhone")
        work_phone.clear()
        work_phone.send_keys(income_data["workPhone"])
        Select(driver.find_element_by_id("EditableIncome_HireDate_Month")).select_by_index(random.randint(1,12))
        Select(driver.find_element_by_id("EditableIncome_HireDate_Year")).select_by_index(random.randint(2,60))
    pay_cycle = Select(driver.find_element_by_id("EditableIncome_PayCycle"))
    pay_cycle.select_by_index(random.randint(1,4))
    time.sleep(2)
    if pay_cycle.first_selected_option.text == "BiWeekly":
        pay_date = driver.find_element_by_id("EditableIncome_LastBiweeklyPayDate")
        pay_date.clear()
        pay_date.send_keys(income_data["paydate"])
    elif pay_cycle.first_selected_option.text == "Weekly":
        Select(driver.find_element_by_id("EditableIncome_WeeklyPayday")).select_by_index(random.randint(1,7))
    elif pay_cycle.first_selected_option.text == "Monthly":
        pay_date = driver.find_element_by_id("EditableIncome_NextMonthlyPayDate")
        pay_date.clear()
        pay_date.send_keys(income_data["paydate"])
        Select(driver.find_element_by_id("EditableIncome_NextMonthlyPayDateMethod")).select_by_index(random.randint(1,2))
    elif pay_cycle.first_selected_option.text == "Twice a month":
        Select(driver.find_element_by_id("EditableIncome_BimonthlyPayday")).select_by_index(random.randint(1,5))

    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='EditableIncome_DirectDeposit_True']//parent::label").click()
    driver.find_element_by_xpath("//*[@id='EditableIncome_IncomeFrequency_Monthly']//parent::label").click()
    driver.find_element_by_id("EditableIncome_GrossPay").clear()
    driver.find_element_by_id("EditableIncome_GrossPay").send_keys(income_data["grossPay"])
    driver.find_element_by_id("EditableIncome_NetPay").clear()
    driver.find_element_by_id("EditableIncome_NetPay").send_keys(income_data["takeHome"])
    time.sleep(3)
    try:
        WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.ID, "btnNext")))
        next_btn = driver.find_element_by_id("btnNext")
        next_btn.click()
    except:
        print("Oops! something went a miss. Please try again...")
        next_btn.click()



def _review_income_details():
    #next_btn = driver.find_element_by_xpath("//button[@type='submit' and @class='btn btn-green btn-lg btn-block']")
    wait = WebDriverWait(driver, 300)
    try:
        page_loaded = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-green btn-lg btn-block']//parent::div")))
        time.sleep(2)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='btnNext']//parent::div")))
            next_btn = driver.find_element_by_id("btnNext")
            next_btn.click()
        except:
            print("Oops! something went a miss. Please try again...")
            next_btn.click()
    except:
        print("Response timed out")



def _fill_bank_details(bank_data):
    try:
        page_loaded =  WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "BankAccount_TransitNumber")))
    except:
        print("Response timed out")
    rout_num = driver.find_element_by_id("BankAccount_TransitNumber")
    rout_num.clear()
    rout_num.send_keys(bank_data["routing"])
    acc_num = driver.find_element_by_id("BankAccount_AccountNumber")
    acc_num.clear()
    acc_num.send_keys(bank_data["account"])
    verify_acc_num = driver.find_element_by_id("BankAccount_AccountNumberVerify")
    verify_acc_num.clear()
    verify_acc_num.send_keys(bank_data["account"])
    card_num = driver.find_element_by_id("Card_Number")
    card_num.clear()
    card_num.send_keys(bank_data["cardnumber"])
    card_num_ver = driver.find_element_by_id("Card_NumberVerification")
    card_num_ver.clear()
    card_num_ver.send_keys(bank_data["cardnumber"])
    Select(driver.find_element_by_id("Card_Expiry_Month")).select_by_index(random.randint(1,12))
    Select(driver.find_element_by_id("Card_Expiry_Year")).select_by_index(random.randint(2,9))
    time.sleep(5)
    next_btn = driver.find_element_by_id("btnNext")
    next_btn.click()



def _fill_apply_now_form(form_data):
    try:
        page_loaded =  WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-home-apply")))
    except:
        print("Response timed out")
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
    email_input.send_keys(str(index)+form_data["email"])
    password_input.send_keys(form_data["password"])
    re_enter_password_input.send_keys(form_data["reenterpassword"])
    security_question_dropdown.select_by_index(random.randint(1,6))
    security_answer_input.send_keys(form_data["securityanswer"])
    security_answer_input.send_keys(Keys.RETURN)

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
    time.sleep(5)


while index <= results.iteration:
    print ("Testing the website %d/%d \n" %(index, results.iteration))
    _main()
    index = index+1
