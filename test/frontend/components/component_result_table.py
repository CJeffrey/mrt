from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .component_base import ComponentBase


class ComponentTableBody:
    """
    The Table body, data of 2 dimension
    """

    def __init__(self, elements: list):
        self.elements = elements

    def __getitem__(self, item):
        return self.elements.__getitem__(item)

    def __len__(self):
        return len(self.elements)


class ComponentTableRow:
    """
    A table row, data of 1 dimension
    """

    def __init__(self, element: WebElement):
        self.element = element

    def __getitem__(self, item):
        return self.element.find_elements_by_tag_name('td').__getitem__(item)


class ComponentTableHead:
    """
    A table head, data of 1 dimension
    """

    def __init__(self, element: WebElement):
        self.element = element

    def __getitem__(self, item):
        return self.element.find_elements_by_tag_name('th').__getitem__(item)


class ComponentResultTable(ComponentBase):
    """
    The result table
    """

    def __init__(self, driver: WebDriver, *args, **kwargs):
        super(ComponentResultTable, self).__init__(driver, *args, **kwargs)
        self.element = self.wait_for_element_by_id('result_table')

    @property
    def head(self) -> ComponentTableHead:
        """
        Get the table head
        """
        return ComponentTableHead(
            self.wait_for_elements_by_tag_name('tr')[0])

    @property
    def body(self) -> ComponentTableBody:
        """
        Get the table body
        """
        res = []
        raw_rows = self.wait_for_elements_by_tag_name('tr')[1:]

        for row in raw_rows:
            res.append(ComponentTableRow(row))

        return ComponentTableBody(res)
