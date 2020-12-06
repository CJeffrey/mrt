from selenium.webdriver.remote.webdriver import WebDriver
from .component_base import ComponentBase


class ComponentMRTLink(ComponentBase):
    """
    A link between two stations
    """

    def __init__(self, driver: WebDriver, element_id: str):
        super(ComponentMRTLink, self).__init__(driver)
        self.element = self.wait_for_element_by_id(element_id)

    def is_activated(self) -> bool:
        """
        Check the stroke color
        """
        return self.element.get_attribute('stroke') != '#D3D3D3'
