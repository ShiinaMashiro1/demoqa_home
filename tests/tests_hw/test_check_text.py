import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.components import BaseComponent  # импортируем класс с методом get_text


@pytest.fixture
def driver():
    """
    Фикстура для запуска и закрытия браузера.
    """
    options = Options()
    options.add_argument("--start-maximized")
    service = ChromeService()  # если chromedriver в PATH
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_footer_text(driver):
    """
    a. перейти на страницу 'https://demoqa.com/'
    b. проверить, что текст в подвале ==
       '© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.'
    """
    driver.get("https://demoqa.com/")

    footer = BaseComponent(
        driver,
        (By.CSS_SELECTOR, "footer .footer-text")  # локатор подвала
    )
    actual_text = footer.get_text()

    assert actual_text == "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.", \
        f"Ожидали: '© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.', получили: {actual_text}"


def test_center_text_on_elements_page(driver):
    """
    a. перейти на страницу 'https://demoqa.com/'
    b. через кнопку перейти на страницу 'https://demoqa.com/elements'
    c. проверить, что текст по центру ==
       'Please select an item from left to start practice.'
    """
    driver.get("https://demoqa.com/")

    # Кнопка "Elements"
    elements_button = BaseComponent(
        driver,
        (By.XPATH, "//h5[text()='Elements']/ancestor::div[contains(@class, 'top-card')]")
    )
    elements_button.click()

    # Центральный текст
    center_text = BaseComponent(
        driver,
        (By.CSS_SELECTOR, ".col-12.mt-4.col-md-6")
    )
    actual_text = center_text.get_text()

    assert actual_text == "Please select an item from left to start practice.", \
        f"Ожидали: 'Please select an item from left to start practice.', получили: {actual_text}"
