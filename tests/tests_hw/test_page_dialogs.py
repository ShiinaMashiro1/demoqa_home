# tests/test_page_dialogs.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.modal_dialogs import ModalDialogsPage


@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--window-size=1000,1000")
    drv = webdriver.Chrome(options=opts)
    try:
        yield drv
    finally:
        drv.quit()


@pytest.mark.ui
def test_modal_elements(driver):
    page = ModalDialogsPage(driver).open()
    assert page.get_submenu_count() == 5, "Ожидали 5 элементов слева"


@pytest.mark.ui
def test_navigation_modal(driver):
    page = ModalDialogsPage(driver).open()

    page.refresh()

    page.click_home_icon()

    driver.back()

    driver.set_window_size(900, 400)

    driver.forward()

    WebDriverWait(driver, 10).until(lambda d: d.current_url.startswith(page.BASE_URL))
    assert driver.current_url.rstrip("/") == page.BASE_URL

    WebDriverWait(driver, 10).until(EC.title_contains("DEMOQA"))
    assert "DEMOQA" in driver.title.upper()

    driver.set_window_size(1000, 1000)
