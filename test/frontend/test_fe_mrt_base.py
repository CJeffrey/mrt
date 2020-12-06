import pytest
from selenium import webdriver


class TestMRTBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown_driver(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        yield

        self.driver.close()

    @property
    def host_url(self):
        return 'http://localhost:5000/'
