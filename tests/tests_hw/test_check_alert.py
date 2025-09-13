import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import browser


@pytest.mark.ui
def test_timer_alert_appears_after_5_seconds(browser):
    browser.get("https://demoqa.com/alerts")
    wait = WebDriverWait(browser, 15)  # запас по времени > 5 сек

    btn = wait.until(EC.element_to_be_clickable((By.ID, "timerAlertButton")))
    btn.click()

    wait.until(EC.alert_is_present())
    alert = browser.switch_to.alert
    alert.accept()
