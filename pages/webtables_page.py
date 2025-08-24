from dataclasses import dataclass
from typing import Optional, List, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class Person:
    first_name: str
    last_name: str
    email: str
    age: str
    salary: str
    department: str


class WebTablesPage:
    URL = "https://demoqa.com/webtables"

    ADD_BTN = (By.ID, "addNewRecordButton")
    SUBMIT_BTN = (By.ID, "submit")
    USER_FORM = (By.ID, "userForm")

    SEARCH_INPUT = (By.ID, "searchBox")
    TABLE_BODY_ROWS = (By.CSS_SELECTOR, "div.rt-tbody div.rt-tr-group")
    NO_ROWS = (By.CSS_SELECTOR, "div.rt-noData")

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    AGE = (By.ID, "age")
    SALARY = (By.ID, "salary")
    DEPARTMENT = (By.ID, "department")

    PAGINATION = (By.CSS_SELECTOR, "div.-pagination")
    PREV_BTN = (By.XPATH, "//button[normalize-space()='Previous']")
    NEXT_BTN = (By.XPATH, "//button[normalize-space()='Next']")

    PAGE_INPUT_CANDIDATES: Tuple[Tuple[str, str], ...] = (
        (By.CSS_SELECTOR, "input.-pageJump"),
        (By.XPATH, "//div[contains(@class,'-pageJump')]//input"),
        (By.XPATH, "//input[@aria-label='jump to page' or @aria-label='Jump to page']"),
        (By.XPATH, "//div[contains(@class,'-pagination')]//input[@type='number']"),
    )

    PAGE_INFO_CANDIDATES: Tuple[Tuple[str, str], ...] = (
        (By.XPATH, "//*[contains(@class,'-pageInfo')]"),
        (By.CSS_SELECTOR, "span.-pageInfo"),
        (By.CSS_SELECTOR, "div.-pageInfo"),
        (By.XPATH, "//input[contains(@class,'-pageJump')]/following-sibling::*[contains(normalize-space(.), 'of ')]"),
        (By.XPATH, "//div[contains(@class,'-pagination')]//*[contains(normalize-space(.), 'of ')]"),
    )

    PAGE_SIZE_SELECTS: Tuple[Tuple[str, str], ...] = (
        (By.CSS_SELECTOR, "div.-pageSizeOptions select"),
        (By.CSS_SELECTOR, "select[aria-label='rows per page']"),
        (By.XPATH, "//select[ancestor::*[contains(@class,'-pageSizeOptions')]]"),
    )

    def __init__(self, browser: WebDriver, timeout: int = 8):
        self.browser = browser
        self.wait = WebDriverWait(browser, timeout)

    def open(self):
        self.browser.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.ADD_BTN))

    def open_add_dialog(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_BTN)).click()
        self.wait.until(EC.visibility_of_element_located(self.USER_FORM))

    def is_dialog_open(self) -> bool:
        els = self.browser.find_elements(*self.USER_FORM)
        return any(el.is_displayed() for el in els)

    def submit_dialog(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BTN)).click()

    def close_dialog_wait(self):
        self.wait.until(EC.invisibility_of_element_located(self.USER_FORM))

    def fill_form(self, person: Person):
        self._clear_and_type(self.FIRST_NAME, person.first_name)
        self._clear_and_type(self.LAST_NAME, person.last_name)
        self._clear_and_type(self.EMAIL, person.email)
        self._clear_and_type(self.AGE, person.age)
        self._clear_and_type(self.SALARY, person.salary)
        self._clear_and_type(self.DEPARTMENT, person.department)

    def search(self, text: str):
        self._clear_and_type(self.SEARCH_INPUT, text)
        self._wait_rows_or_no_rows()

    def clear_search(self):
        el = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        el.clear()
        self._wait_rows_or_no_rows()

    def has_no_rows_message(self) -> bool:
        els = self.browser.find_elements(*self.NO_ROWS)
        return any(el.is_displayed() for el in els)

    def get_all_rows(self) -> List[WebElement]:
        return self.browser.find_elements(*self.TABLE_BODY_ROWS)

    def find_row_by_email(self, email: str) -> Optional[WebElement]:
        self.search(email)
        if self.has_no_rows_message():
            return None
        for row in self.get_all_rows():
            if email in row.text:
                return row
        return None

    def row_texts(self, row: WebElement) -> List[str]:
        cells = row.find_elements(By.CSS_SELECTOR, ".rt-td")
        return [c.text.strip() for c in cells]

    def click_edit_in_row(self, row: WebElement):
        row.find_element(By.CSS_SELECTOR, "span[title='Edit']").click()
        self.wait.until(EC.visibility_of_element_located(self.USER_FORM))

    def click_delete_in_row(self, row: WebElement):
        row.find_element(By.CSS_SELECTOR, "span[title='Delete']").click()
        self._wait_rows_or_no_rows()

    def set_rows_per_page(self, value: int):
        select_el = self._find_first_present(self.PAGE_SIZE_SELECTS)
        sel = Select(select_el)
        for opt in sel.options:
            if opt.text.strip().startswith(str(value)):
                sel.select_by_visible_text(opt.text)
                break
        self._wait_rows_or_no_rows()

    def get_current_page(self) -> int:
        self._scroll_pagination_into_view()
        val = self._read_current_page_value_no_wait()
        if val is not None:
            return val
        # резервная эвристика
        if self.is_prev_disabled() and self.is_next_disabled():
            return 1
        return 1

    def get_total_pages(self) -> int:
        text = self._try_get_page_info_text()
        if text:
            parts = text.strip().split()
            for token in reversed(parts):
                if token.isdigit():
                    return int(token)
        try:
            if self.get_current_page() == 1 and self.is_prev_disabled() and self.is_next_disabled():
                return 1
        except Exception:
            pass
        return 1

    def is_next_disabled(self) -> bool:
        btn = self.wait.until(EC.presence_of_element_located(self.NEXT_BTN))
        return self._is_button_disabled(btn)

    def is_prev_disabled(self) -> bool:
        btn = self.wait.until(EC.presence_of_element_located(self.PREV_BTN))
        return self._is_button_disabled(btn)

    def click_next(self):
        self._scroll_pagination_into_view()
        before_page = self._read_current_page_value_no_wait()
        before_sig = self._rows_signature()
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BTN)).click()
        self._wait_page_changed(before_page, before_sig)

    def click_prev(self):
        self._scroll_pagination_into_view()
        before_page = self._read_current_page_value_no_wait()
        before_sig = self._rows_signature()
        self.wait.until(EC.element_to_be_clickable(self.PREV_BTN)).click()
        self._wait_page_changed(before_page, before_sig)

    def _clear_and_type(self, locator, text: str):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.clear()
        el.send_keys(text)

    def _is_button_disabled(self, btn: WebElement) -> bool:
        disabled_attr = btn.get_attribute("disabled")
        aria_disabled = btn.get_attribute("aria-disabled")
        cls = btn.get_attribute("class") or ""
        return (
            disabled_attr is not None
            or (aria_disabled and aria_disabled.lower() == "true")
            or ("-disabled" in cls or " disabled" in f" {cls} ")
        )

    def _find_first_present(self, locator_candidates: Tuple[Tuple[str, str], ...]) -> WebElement:
        last_exc = None
        for by, sel in locator_candidates:
            try:
                return WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((by, sel)))
            except Exception as e:
                last_exc = e
        raise last_exc

    def _is_no_rows_visible(self) -> bool:
        els = self.browser.find_elements(*self.NO_ROWS)
        return any(el.is_displayed() for el in els)

    def _rows_count(self) -> int:
        return len(self.browser.find_elements(*self.TABLE_BODY_ROWS))

    def _wait_rows_or_no_rows(self):
        self.wait.until(lambda d: self._rows_count() > 0 or self._is_no_rows_visible())

    def _scroll_pagination_into_view(self):
        try:
            el = self._find_first_present((self.PAGINATION,))
            self.browser.execute_script("arguments[0].scrollIntoView({block:'end'});", el)
        except Exception:
            # не критично, просто продолжаем
            pass

    def _try_get_page_info_text(self) -> Optional[str]:
        for by, sel in self.PAGE_INFO_CANDIDATES:
            els = self.browser.find_elements(by, sel)
            for el in els:
                txt = (el.text or "").strip()
                if txt and "of" in txt:
                    return txt
        for by, sel in self.PAGE_INFO_CANDIDATES:
            try:
                el = WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((by, sel)))
                txt = (el.text or "").strip()
                if txt and "of" in txt:
                    return txt
            except Exception:
                continue
        return None

    def _read_current_page_value_no_wait(self) -> Optional[int]:
        for by, sel in self.PAGE_INPUT_CANDIDATES:
            els = self.browser.find_elements(by, sel)
            for el in els:
                val = (el.get_attribute("value") or "").strip()
                if not val:
                    try:
                        val = (self.browser.execute_script("return arguments[0].value;", el) or "").strip()
                    except Exception:
                        val = ""
                if val.isdigit():
                    return int(val)
        for by, sel in self.PAGE_INPUT_CANDIDATES:
            try:
                el = WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((by, sel)))
                val = (el.get_attribute("value") or "").strip()
                if not val:
                    try:
                        val = (self.browser.execute_script("return arguments[0].value;", el) or "").strip()
                    except Exception:
                        val = ""
                if val.isdigit():
                    return int(val)
            except Exception:
                continue
        return None

    def _rows_signature(self) -> str:
        rows = self.get_all_rows()
        sig_parts: List[str] = []
        for r in rows[:3]:
            cells = r.find_elements(By.CSS_SELECTOR, ".rt-td")
            sig_parts.append("|".join(c.text.strip() for c in cells[:3]))
        return "||".join(sig_parts)

    def _wait_page_changed(self, before_page: Optional[int], before_sig: str):
        def changed(_):
            now_page = self._read_current_page_value_no_wait()
            now_sig = self._rows_signature()
            page_changed = (before_page is None) or (now_page is not None and now_page != before_page)
            sig_changed = now_sig != before_sig
            return page_changed or sig_changed

        self.wait.until(changed)
        self._wait_rows_or_no_rows()
