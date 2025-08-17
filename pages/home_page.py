from selenium.webdriver.common.by import By
from .components import BaseComponent


class HomePage:
    URL = "https://demoqa.com/"

    FOOTER_TEXT = (By.XPATH, "//footer//*[contains(., 'ALL RIGHTS RESERVED')]")
    ELEMENTS_CARD = (By.XPATH, "//h5[normalize-space(.)='Elements']/ancestor::div[contains(@class,'top-card')]")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def footer(self):
        return BaseComponent(self.driver, self.FOOTER_TEXT)

    def elements_card(self):
        return BaseComponent(self.driver, self.ELEMENTS_CARD)
