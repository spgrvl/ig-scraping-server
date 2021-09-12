import time
import sys
import getpass

def login(driver):
    login_url = "https://www.instagram.com/accounts/login/"
    driver.get(login_url)    
    time.sleep(3)

    # Click Accept in cookies banner
    buttons = driver.find_elements_by_tag_name('button')
    for button in buttons:
        if button.text == "Accept All":
            button.click()
            break

    username_field = driver.find_element_by_name("username")
    username_field.send_keys(input("Enter Instagram Username: "))
    time.sleep(0.5)
    
    password_field = driver.find_element_by_name("password")
    password_field.send_keys(getpass.getpass("Enter Instagram Password: "))
    time.sleep(0.5)
    
    login_button = driver.find_element_by_css_selector("[type^=submit]")
    login_button.click()
    time.sleep(5)

    try:
        unusual_login = driver.find_element_by_tag_name('h2').text
        if unusual_login == "We Detected An Unusual Login Attempt":
            code_login(driver)
    except:
        pass
    finally:
        time.sleep(5)
        login_status(driver)

def login_status(driver):
    try:
        driver.find_element_by_css_selector("[data-testid^=user-avatar]")
        print("Instagram login done!\n")
    except:
        driver.quit()
        sys.exit("Failed to login, exiting!")

def code_login(driver):
    print("Instagram: Unusual Login Attempt Detected!")
    code_buttons = driver.find_elements_by_tag_name('button')
    for button in code_buttons:
        if button.text == "Send Security Code":
            button.click()
            break
    time.sleep(3)

    code_field = driver.find_element_by_tag_name('input')
    code_field.send_keys(input("Enter the 6 digit code Instagram emailed you: "))

    submit_buttons = driver.find_elements_by_tag_name('button')
    for button in submit_buttons:
        if button.text == "Submit":
            button.click()
            break