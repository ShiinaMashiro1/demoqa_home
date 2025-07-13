from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TextSearch(BasePage):
    def __init__(self, driver,):
        self.url = 'https://demoqa.com/'
        super().__init__(driver, self.url)
    def get_text(self):
        text = str(self.driver.find_element(locator= '#app > footer > a').text)
        return text