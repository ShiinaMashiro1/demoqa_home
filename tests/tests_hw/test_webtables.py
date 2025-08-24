import random
import string
import pytest

from pages.webtables_page import WebTablesPage, Person
from conftest import browser


def _rand(n=6) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


@pytest.mark.ui
def test_webtables_add_edit_delete(browser):

    page = WebTablesPage(browser)
    page.open()

    page.open_add_dialog()

    page.submit_dialog()
    assert page.is_dialog_open(), "Пустая форма не должна сохраняться (диалог не должен закрываться)."

    unique_email = f"ivan.petrov.{_rand()}@mail.com"
    person = Person(
        first_name="Ivan",
        last_name="Petrov",
        email=unique_email,
        age="35",
        salary="5000",
        department="QA"
    )
    page.fill_form(person)
    page.submit_dialog()
    page.close_dialog_wait()

    row = page.find_row_by_email(person.email)
    assert row is not None, "После сохранения запись не найдена в таблице по email."
    row_text = page.row_texts(row)
    assert person.first_name in row_text[0]
    assert person.last_name in row_text[1]
    assert person.age in row_text[2]
    assert person.email in row_text[3]
    assert person.salary in row_text[4]
    assert person.department in row_text[5]

    page.click_edit_in_row(row)
    assert page.is_dialog_open(), "Диалог редактирования не открылся."

    assert browser.find_element(*page.FIRST_NAME).get_attribute("value") == person.first_name
    assert browser.find_element(*page.EMAIL).get_attribute("value") == person.email

    new_first_name = "Petr"
    browser.find_element(*page.FIRST_NAME).clear()
    browser.find_element(*page.FIRST_NAME).send_keys(new_first_name)
    page.submit_dialog()
    page.close_dialog_wait()

    page.clear_search()
    row = page.find_row_by_email(person.email)
    assert row is not None, "После обновления запись по email исчезла — так быть не должно."
    row_text = page.row_texts(row)
    assert row_text[0] == new_first_name, "Имя в таблице не обновилось после редактирования."

    page.click_delete_in_row(row)
    page.clear_search()
    row = page.find_row_by_email(person.email)
    assert row is None and page.has_no_rows_message(), "После удаления запись всё ещё видна в таблице."


@pytest.mark.ui
def test_webtables_pagination_controls(browser):
    page = WebTablesPage(browser)
    page.open()
    page.set_rows_per_page(5)

    assert page.is_prev_disabled(), "Кнопка Previous должна быть заблокирована при одной странице."
    assert page.is_next_disabled(), "Кнопка Next должна быть заблокирована при одной странице."
    assert page.get_total_pages() == 1, "Ожидали 1 страницу до добавления новых записей."

    for i in range(3):
        page.open_add_dialog()
        p = Person(
            first_name=f"Name{i}",
            last_name=f"Surname{i}",
            email=f"test{i}.{_rand()}@mail.com",
            age=str(20 + i),
            salary=str(3000 + i * 100),
            department="QA"
        )
        page.fill_form(p)
        page.submit_dialog()
        page.close_dialog_wait()

    total_pages = page.get_total_pages()
    assert total_pages == 2, f"После добавления 3 записей ожидали 'of 2', но получили 'of {total_pages}'."
    assert not page.is_next_disabled(), "Кнопка Next должна стать доступной при наличии второй страницы."

    page.click_next()
    assert page.get_current_page() == 2, "После клика Next должны быть на странице 2."

    page.click_prev()
    assert page.get_current_page() == 1, "После клика Previous должны вернуться на страницу 1."
