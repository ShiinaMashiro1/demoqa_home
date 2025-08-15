import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.components import BaseComponent


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = ChromeService()
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


def test_footer_text(driver):
    driver.get("https://demoqa.com/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".category-cards"))
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    footer_text_comp = BaseComponent(
        driver,
        (By.XPATH, "//footer//*[contains(., 'ALL RIGHTS RESERVED')]")
    )

    actual_text = footer_text_comp.get_text().strip()
    expected = "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."
    assert actual_text == expected, f"Ожидали: {expected!r}, получили: {actual_text!r}"


def test_center_text_on_elements_page(driver):
    driver.get("https://demoqa.com/")

    elements_card = BaseComponent(
        driver,
        (By.XPATH, "//h5[normalize-space(.)='Elements']/ancestor::div[contains(@class,'top-card')]")
    )

    elements_card.click()
    WebDriverWait(driver, 10).until(EC.url_contains("/elements"))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'col-12') and contains(@class,'mt-4') and contains(@class,'col-md-6')]")
        )
    )

    center_text_comp = BaseComponent(
        driver,
        (By.XPATH, "//div[contains(@class,'col-12') and contains(@class,'mt-4') and contains(@class,'col-md-6')]")
    )
    actual_text = center_text_comp.get_text().strip()

    expected = "Please select an item from left to start practice."
    assert actual_text == expected, f"Ожидали: {expected!r}, получили: {actual_text!r}"
