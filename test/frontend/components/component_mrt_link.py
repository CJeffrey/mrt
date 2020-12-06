from selenium.webdriver.remote.webdriver import WebDriver


class ComponentMRTLink:
    def __init__(self, driver: WebDriver, element_id: str):
        self.element = driver.find_element_by_id(element_id)

    def is_activated(self):
        return self.element.get_attribute('stroke') != '#D3D3D3'
