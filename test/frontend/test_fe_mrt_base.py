import pytest
from selenium import webdriver


class TestMRTBase:
    @pytest.fixture(scope='function')
    def driver(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver

        driver.close()

    @property
    def host_url(self):
        return 'http://localhost:5000/'
