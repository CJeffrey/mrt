from .test_fe_mrt_base import TestMRTBase


class TestFEMainPage(TestMRTBase):
    def test_main_page(self, driver):
        driver.get(self.host_url)
        h1 = driver.find_element_by_css_selector("h1")
        assert h1.text == 'Welcome to MRT Search System'
