# pages/accordion.py
from selenium.webdriver.common.by import By


class Accordion:
    URL = "https://demoqa.com/accordian"

    SECTION1_CONTENT_P = (By.CSS_SELECTOR, "#section1Content > p")
    SECTION1_HEADING = (By.CSS_SELECTOR, "#section1Heading")

    SECTION2_CONTENT_P1 = (By.CSS_SELECTOR, "#section2Content > p:nth-child(1)")
    SECTION2_CONTENT_P2 = (By.CSS_SELECTOR, "#section2Content > p:nth-child(2)")
    SECTION3_CONTENT_P = (By.CSS_SELECTOR, "#section3Content > p")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    @property
    def section1_content_p(self):
        return self.driver.find_element(*self.SECTION1_CONTENT_P)

    @property
    def section1_heading(self):
        return self.driver.find_element(*self.SECTION1_HEADING)

    @property
    def section2_content_p1(self):
        return self.driver.find_element(*self.SECTION2_CONTENT_P1)

    @property
    def section2_content_p2(self):
        return self.driver.find_element(*self.SECTION2_CONTENT_P2)

    @property
    def section3_content_p(self):
        return self.driver.find_element(*self.SECTION3_CONTENT_P)
