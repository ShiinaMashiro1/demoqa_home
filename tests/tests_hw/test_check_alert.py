import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import browser

@pytest.mark.ui
def test_timer_alert(browser):
    url = "https://demoqa.com/alerts"
    browser.get(url)
    wait = WebDriverWait(browser, 10)

    timer_btn = wait.until(EC.element_to_be_clickable((By.ID, "timerAlertButton")))
    timer_btn.click()

    alert = wait.until(EC.alert_is_present())

    alert_text = alert.text
    assert "alert" in alert_text.lower(), f"Неожиданный текст алерта: {alert_text}"

    alert.accept()
