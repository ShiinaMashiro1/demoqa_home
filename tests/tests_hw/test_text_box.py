import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest   import browser


def _hide_overlays(browser):
    # Прячем баннеры/куки, которые иногда перекрывают кнопку Submit
    browser.execute_script("""
        const ids = ['fixedban','adplus-anchor'];
        ids.forEach(id => { const el = document.getElementById(id); if (el) el.style.display = 'none'; });
        const cn = document.getElementsByClassName('fc-consent-root');
        if (cn && cn[0]) cn[0].style.display = 'none';
    """)


@pytest.mark.ui
def test_text_box_submit_shows_text(browser):
    """
    a. перейти на /text-box
    b. записать в поля Full Name и Current Address произвольный текст (через переменные)
    c. нажать Submit
    d. проверить, что в блоке Output текст совпадает с введённым
    """
    browser.get("https://demoqa.com/text-box")
    wait = WebDriverWait(browser, 10)
    _hide_overlays(browser)

    # значения через переменные
    full_name_value = "Иван Петров"
    current_address_value = "г. Казань, ул. Пушкина, д. 10"

    # элементы формы
    name_input = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
    current_addr_input = browser.find_element(By.ID, "currentAddress")
    submit_btn = browser.find_element(By.ID, "submit")

    # ввод
    name_input.clear()
    name_input.send_keys(full_name_value)
    current_addr_input.clear()
    current_addr_input.send_keys(current_address_value)

    # клик сабмита (на всякий случай — скроллим к элементу)
    browser.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
    submit_btn.click()

    # проверки
    output = wait.until(EC.visibility_of_element_located((By.ID, "output")))
    name_out = output.find_element(By.CSS_SELECTOR, "#name")
    curr_addr_out = output.find_element(By.CSS_SELECTOR, "#currentAddress")

    def right_of_colon(text: str) -> str:
        return text.split(":", 1)[1].strip() if ":" in text else text.strip()

    assert right_of_colon(name_out.text) == full_name_value
    assert right_of_colon(curr_addr_out.text) == current_address_value
