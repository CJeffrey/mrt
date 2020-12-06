from selenium.webdriver.remote.webdriver import WebDriver


class ComponentMRTMap:
    def __init__(self, driver: WebDriver):
        driver.find_element_by_id('svg_map')
