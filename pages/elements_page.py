from selenium.webdriver.common.by import By
from .components import BaseComponent


class ElementsPage:
    CENTER_TEXT = (By.CSS_SELECTOR, ".col-12.mt-4.col-md-6")

    def __init__(self, driver):
        self.driver = driver

    def center_text(self):
        return BaseComponent(self.driver, self.CENTER_TEXT)
