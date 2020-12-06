from selenium.webdriver.remote.webdriver import WebDriver
from .component_base import ComponentBase


class ComponentSearchForm(ComponentBase):
    """
    The search form
    """

    def __init__(self, driver: WebDriver):
        super(ComponentSearchForm, self).__init__(driver)
        self.element = self.wait_for_element_by_id('search_form')

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
