from selenium.webdriver.remote.webdriver import WebDriver
from .component_base import ComponentBase


class ComponentMRTMap(ComponentBase):
    """
    The mrt map
    """
    def __init__(self, driver: WebDriver):
        super(ComponentMRTMap, self).__init__(driver)
        self.element = self.wait_for_element_by_id('svg_map')
