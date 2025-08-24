import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import browser


def _hide_overlays(browser):
    browser.execute_script("""
        const ids = ['fixedban','adplus-anchor'];
        ids.forEach(id => { const el = document.getElementById(id); if (el) el.style.display = 'none'; });
        const cn = document.getElementsByClassName('fc-consent-root');
        if (cn && cn[0]) cn[0].style.display = 'none';
    """)


@pytest.mark.ui
def test_fill_state_and_city(browser):
    browser.get("https://demoqa.com/automation-practice-form")
    wait = WebDriverWait(browser, 10)
    _hide_overlays(browser)

    state_container = wait.until(EC.element_to_be_clickable((By.ID, "state")))
    browser.execute_script("arguments[0].scrollIntoView({block:'center'});", state_container)
    state_container.click()
    state_input = wait.until(EC.presence_of_element_located((By.ID, "react-select-3-input")))
    state_input.send_keys("NCR")
    state_input.send_keys(Keys.ENTER)

    city_container = wait.until(EC.element_to_be_clickable((By.ID, "city")))
    browser.execute_script("arguments[0].scrollIntoView({block:'center'});", city_container)
    city_container.click()
    city_input = wait.until(EC.presence_of_element_located((By.ID, "react-select-4-input")))
    city_input.send_keys("Delhi")
    city_input.send_keys(Keys.ENTER)

    state_value = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="state"]//div[contains(@class,"singleValue")]'))).text
    city_value = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="city"]//div[contains(@class,"singleValue")]'))).text

    assert state_value == "NCR"
    assert city_value == "Delhi"
