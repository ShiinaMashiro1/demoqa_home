import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest   import browser


def _hide_overlays(browser):
    browser.execute_script("""
        const ids = ['fixedban','adplus-anchor'];
        ids.forEach(id => { const el = document.getElementById(id); if (el) el.style.display = 'none'; });
        const cn = document.getElementsByClassName('fc-consent-root');
        if (cn && cn[0]) cn[0].style.display = 'none';
    """)


@pytest.mark.ui
def test_text_box_submit_shows_text(browser):
    browser.get("https://demoqa.com/text-box")
    wait = WebDriverWait(browser, 10)
    _hide_overlays(browser)

    full_name_value = "User Name"
    current_address_value = "User Address"

    name_input = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
    current_addr_input = browser.find_element(By.ID, "currentAddress")
    submit_btn = browser.find_element(By.ID, "submit")

    name_input.clear()
    name_input.send_keys(full_name_value)
    current_addr_input.clear()
    current_addr_input.send_keys(current_address_value)

    browser.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
    submit_btn.click()

    output = wait.until(EC.visibility_of_element_located((By.ID, "output")))
    name_out = output.find_element(By.CSS_SELECTOR, "#name")
    curr_addr_out = output.find_element(By.CSS_SELECTOR, "#currentAddress")

    def right_of_colon(text: str) -> str:
        return text.split(":", 1)[1].strip() if ":" in text else text.strip()

    assert right_of_colon(name_out.text) == full_name_value
    assert right_of_colon(curr_addr_out.text) == current_address_value
