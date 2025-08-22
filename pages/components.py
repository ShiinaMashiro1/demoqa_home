from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseComponent:
    def __init__(self, driver, locator, timeout=10):
        self.driver = driver
        self.locator = locator
        self.timeout = timeout

    def find_element(self):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(self.locator)
        )

    def click(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.locator)
        ).click()

    def get_text(self):
        return self.find_element().text.strip()