from selenium.common import NoSuchElementException
from pages.base_page import BasePage


class SwagLabs(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)

    def exist_icon(self):
        try:
            self.find_element(locator='div.login_logo')
        except NoSuchElementException:
            return False
        return True


