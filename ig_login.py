import time

def login(driver):
    login_url = "https://www.instagram.com/accounts/login/"
    driver.get(login_url)    
    time.sleep(3)

    buttons = driver.find_elements_by_tag_name('button')
    for button in buttons:
        if button.text == "Accept":
            button.click()
            break

    username_field = driver.find_element_by_name("username")
    username_field.send_keys(input("Enter Instagram Username: "))
    time.sleep(0.5)
    
    password_field = driver.find_element_by_name("password")
    password_field.send_keys(input("Enter Instagram Password: "))
    time.sleep(0.5)
    
    login_button = driver.find_element_by_css_selector("[type^=submit]")
    login_button.click()
    print("Instagram login done!")