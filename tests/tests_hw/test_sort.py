import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import browser


@pytest.mark.ui
def test_webtables_sort_by_each_sortable_header(browser):
    browser.get("https://demoqa.com/webtables")
    wait = WebDriverWait(browser, 10)

    headers = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.rt-table div.rt-thead.-header .rt-th")
        )
    )

    assert headers, "Заголовки таблицы не найдены"

    for th in headers:
        name = th.text.strip()
        if name.lower() == "action":
            continue

        th.click()

        def _sorted_class_present(_):
            classes = th.get_attribute("class") or ""
            return "-sort-asc" in classes or "-sort-desc" in classes

        wait.until(_sorted_class_present)
        first_state = th.get_attribute("class")

        assert any(s in first_state for s in ("-sort-asc", "-sort-desc")), \
            f"После клика по '{name}' класс не содержит -sort-asc/-sort-desc: {first_state}"

        th.click()
        wait.until(
            lambda _: th.get_attribute("class") != first_state
            and any(s in th.get_attribute("class") for s in ("-sort-asc", "-sort-desc"))
        )
