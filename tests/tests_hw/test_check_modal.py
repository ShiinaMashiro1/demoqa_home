import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import browser


URL = "https://demoqa.com/modal-dialogs"


def _is_url_available(url: str, timeout: int = 5) -> bool:
    try:
        import requests
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        if resp.status_code >= 400:
            resp = requests.get(url, timeout=timeout, allow_redirects=True)
        return 200 <= resp.status_code < 400
    except Exception:
        return True


@pytest.mark.ui
def test_modal_windows_open_and_close(browser):
    if not _is_url_available(URL):
        pytest.skip("Страница недоступна (HTTP не 2xx/3xx) — пропускаем тест.")

    browser.get(URL)
    wait = WebDriverWait(browser, 10)
    small_btn = (By.ID, "showSmallModal")
    large_btn = (By.ID, "showLargeModal")
    title_small = (By.ID, "example-modal-sizes-title-sm")
    title_large = (By.ID, "example-modal-sizes-title-lg")
    close_small = (By.ID, "closeSmallModal")
    close_large = (By.ID, "closeLargeModal")

    wait.until(EC.element_to_be_clickable(small_btn))
    wait.until(EC.element_to_be_clickable(large_btn))

    browser.find_element(*small_btn).click()
    wait.until(EC.visibility_of_element_located(title_small))
    browser.find_element(*close_small).click()
    wait.until(EC.invisibility_of_element_located(title_small))

    browser.find_element(*large_btn).click()
    wait.until(EC.visibility_of_element_located(title_large))
    browser.find_element(*close_large).click()
    wait.until(EC.invisibility_of_element_located(title_large))