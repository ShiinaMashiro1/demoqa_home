import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

from pages.home_page import HomePage
from pages.elements_page import ElementsPage


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=ChromeService(), options=options)
    yield driver
    driver.quit()


def test_footer_text(driver):
    home = HomePage(driver)
    home.open()

    actual = home.footer().get_text()
    expected = "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."

    assert actual == expected, f"Ожидали {expected!r}, получили {actual!r}"


def test_center_text_on_elements_page(driver):
    home = HomePage(driver)
    home.open()
    home.elements_card().click()

    elements_page = ElementsPage(driver)
    actual = elements_page.center_text().get_text()
    expected = "Please select an item from left to start practice."

    assert actual == expected, f"Ожидали {expected!r}, получили {actual!r}"
