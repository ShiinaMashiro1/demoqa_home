from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ModalDialogsPage:
    BASE_URL = "https://demoqa.com"
    PATH = "/modal-dialogs"
    SUBMENU_ITEMS = (By.CSS_SELECTOR, ".left-pannel .element-list.collapse.show li")
    HOME_ICON = (By.CSS_SELECTOR,
                 "a.navbar-brand, header a.navbar-brand, "
                 "a[href='/'], a[href='https://demoqa.com']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def open(self):
        self.driver.get(self.BASE_URL + self.PATH)
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(self.SUBMENU_ITEMS)
        )
        return self

    def refresh(self):
        self.driver.refresh()
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(self.SUBMENU_ITEMS)
        )

    def click_home_icon(self):
        # уберем возможный баннер, мешающий клику
        try:
            self.driver.find_element(By.ID, "close-fixedban").click()
        except Exception:
            pass

        wait = WebDriverWait(self.driver, self.timeout)

        try:
            el = wait.until(EC.presence_of_element_located(self.HOME_ICON))
        except TimeoutException:
            el = self.driver.execute_script(
                "return document.querySelector(\"a.navbar-brand, header a.navbar-brand, "
                "a[href='/'], a[href='https://demoqa.com']\");"
            )
            if not el:
                raise

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            wait.until(EC.element_to_be_clickable(self.HOME_ICON)).click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def get_submenu_count(self) -> int:
        return sum(1 for e in self.driver.find_elements(*self.SUBMENU_ITEMS) if e.is_displayed())
