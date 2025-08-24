import pytest
from selenium.webdriver.common.by import By
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
def test_placeholders_and_pattern_then_validate_class(browser):
    browser.get("https://demoqa.com/automation-practice-form")
    wait = WebDriverWait(browser, 10)
    _hide_overlays(browser)

    first_name = wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
    last_name = browser.find_element(By.ID, "lastName")
    user_email = browser.find_element(By.ID, "userEmail")

    assert first_name.get_attribute("placeholder") == "First Name"
    assert last_name.get_attribute("placeholder") == "Last Name"
    assert user_email.get_attribute("placeholder") == "name@example.com"

    pattern = user_email.get_attribute("pattern")
    assert pattern is not None and "@" in pattern, f"Ожидали email-pattern, получили: {pattern!r}"

    submit_btn = browser.find_element(By.ID, "submit")
    browser.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
    submit_btn.click()

    form = browser.find_element(By.ID, "userForm")
    wait.until(lambda d: "was-validated" in form.get_attribute("class"))
    assert "was-validated" in form.get_attribute("class")
