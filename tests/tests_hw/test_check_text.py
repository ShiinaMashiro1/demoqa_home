from selenium.webdriver.common.by import By
from pages.get_text import TextSearch
from conftest import browser

def test_check_elements(browser):
    browser.get('https://demoqa.com/')
    basement = TextSearch(browser)
    basement.get_text()
    assert basement == "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.", "Текст не совпадает"