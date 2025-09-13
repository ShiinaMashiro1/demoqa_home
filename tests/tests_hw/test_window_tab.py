import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import browser

@pytest.mark.ui
def  test_home_link_open_new_tab(browser):
    browser.get('https://demoqa.com/links')
    wait = WebDriverWait(browser, 10)
    link = wait.until(EC.element_to_be_clickable((By.ID, "simpleLink")))

    assert link.text.strip() == "Home", f"Ожидали текст 'Home', получили '{link.text.strip()}'"

    href = link.get_attribute("href") or ""
    assert href.startswith("https://demoqa.com"), f"Неверный href: {href}"

    old_handles = browser.window_handles
    link.click()

    wait.until(lambda d: len(d.window_handles) > len(old_handles))
    new_handle = [h for h in browser.window_handles if h not in old_handles][0]

    browser.switch_to.window(new_handle)
    try:
        current = browser.current_url
        assert current.startswith("https://demoqa.com"), f"Новая вкладка открылась на другой URL: {current}"

    finally:
        browser.close()
        browser.switch_to.window(old_handles[0])
