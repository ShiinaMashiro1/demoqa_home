import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import browser


@pytest.mark.ui
def test_modal_windows_open_and_close(browser):
    url = "https://demoqa.com/modal-dialogs"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            pytest.skip(f"Страница {url} недоступна, статус {response.status_code}")
    except requests.RequestException:
        pytest.skip(f"Страница {url} недоступна")

    browser.get(url)
    wait = WebDriverWait(browser, 10)

    small_modal_btn = wait.until(EC.element_to_be_clickable((By.ID, "showSmallModal")))
    small_modal_btn.click()

    modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
    assert modal.is_displayed(), "Small modal не открылось"

    close_btn = modal.find_element(By.ID, "closeSmallModal")
    close_btn.click()
    wait.until(EC.invisibility_of_element(modal))

    large_modal_btn = wait.until(EC.element_to_be_clickable((By.ID, "showLargeModal")))
    large_modal_btn.click()

    modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
    assert modal.is_displayed(), "Large modal не открылось"

    close_btn = modal.find_element(By.ID, "closeLargeModal")
    close_btn.click()
    wait.until(EC.invisibility_of_element(modal))
