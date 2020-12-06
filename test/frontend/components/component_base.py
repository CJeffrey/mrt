from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.common.by import By


class ComponentBase:
    def __init__(self, driver: WebDriver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=timeout)

    def wait_for_element_by_id(self, e_id):
        return self.wait.until(presence_of_element_located((By.ID, e_id), ))

    def wait_for_elements_by_tag_name(self, e_tag):
        return self.wait.until(presence_of_all_elements_located((By.TAG_NAME, e_tag), ))
