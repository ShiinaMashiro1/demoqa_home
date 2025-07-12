from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver, url='https://www.saucedemo.com/'):
        self.driver = driver
        self.url = url
    def visit(self):
        self.driver.get(self.url)
    def find_element(self, locator):
        return self.driver.find_element(*locator)

