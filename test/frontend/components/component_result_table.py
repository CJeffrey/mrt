from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class ComponentTableBody:
    def __init__(self, elements: list):
        self.elements = elements

    def __getitem__(self, item):
        return self.elements.__getitem__(item)


class ComponentTableRow:
    def __init__(self, element: WebElement):
        self.element = element

    def __getitem__(self, item):
        return self.element.find_elements_by_tag_name('td').__getitem__(item)


class ComponentTableHead:
    def __init__(self, element: WebElement):
        self.element = element

    def __getitem__(self, item):
        return self.element.find_elements_by_tag_name('th').__getitem__(item)


class ComponentResultTable:
    def __init__(self, driver: WebDriver):
        self.element = driver.find_element_by_id('result_table')

    @property
    def head(self):
        return ComponentTableHead(self.element.find_elements_by_tag_name('tr')[0])

    @property
    def body(self):
        res = []
        raw_rows = self.element.find_elements_by_tag_name('tr')[1:]

        for row in raw_rows:
            res.append(ComponentTableRow(row))

        return res
