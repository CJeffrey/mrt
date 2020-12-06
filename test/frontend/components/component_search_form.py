from selenium.webdriver.remote.webdriver import WebDriver


class ComponentSearchForm:
    def __init__(self, driver: WebDriver):
        self.element = driver.find_element_by_id('search_form')

    @property
    def src_name(self):
        return self.element.find_element_by_id('src_name')

    @property
    def des_name(self):
        return self.element.find_element_by_id('des_name')

    @property
    def time(self):
        return self.element.find_element_by_id('time')

    @property
    def submit(self):
        return self.element.find_element_by_id('submit')
