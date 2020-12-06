import pytest

from .test_fe_mrt_base import TestMRTBase


class TestFESearchBasic(TestMRTBase):
    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown_method(self):
        self.url = self.host_url + 'search_basic'

    def test_search_basic_get(self):
        self.driver.get(self.url)
        import time
        time.sleep(111)
