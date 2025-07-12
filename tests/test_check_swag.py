from selenium.webdriver.common.by import By

def test_check_elements(browser):
    browser.get("https://www.saucedemo.com/")
    user_field = browser.find_element(By.ID, "user-name")
    password = browser.find_element(By.ID, "password")
    sub_button = browser.find_element(By.ID, "login-button")
    a = 1 if user_field.is_displayed() else 0
    b = 1 if password.is_displayed() else 0
    c = 1 if sub_button.is_displayed() else 0

    assert a+b+c==3, "Элементы не найдены V2.0"

    if a+b+c==3:
        print("Элементы найдены")
    print("Элементы найдены V2.0") if (user_field.is_displayed() and password.is_displayed() and sub_button.is_displayed())\
        else print("Элементы не найдены V2.0")