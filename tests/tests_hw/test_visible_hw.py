# tests/test_visible_hw.py
import time
import pytest

from pages.accordion import Accordion
from tests.conftest import browser


@pytest.mark.usefixtures("browser")
def test_visible_accordion(browser):
    page = Accordion(browser)
    page.open()

    assert page.section1_content_p.is_displayed(), (
        "Ожидали, что параграф в секции 1 будет видимым по умолчанию."
    )

    page.section1_heading.click()

    time.sleep(2)

    assert not page.section1_content_p.is_displayed(), (
        "Ожидали, что параграф в секции 1 станет скрытым после клика по заголовку."
    )


@pytest.mark.usefixtures("browser")
def test_visible_accordion_default(browser):
    page = Accordion(browser)
    page.open()

    assert not page.section2_content_p1.is_displayed(), (
        "Ожидали, что section2 п.1 скрыт по умолчанию."
    )
    assert not page.section2_content_p2.is_displayed(), (
        "Ожидали, что section2 п.2 скрыт по умолчанию."
    )
    assert not page.section3_content_p.is_displayed(), (
        "Ожидали, что section3 параграф скрыт по умолчанию."
    )