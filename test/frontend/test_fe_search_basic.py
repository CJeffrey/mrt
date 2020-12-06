import pytest
from selenium.common.exceptions import NoSuchElementException

from .test_fe_mrt_base import TestMRTBase
from .components.component_mrt_map import ComponentMRTMap
from .components.component_mrt_link import ComponentMRTLink
from .components.component_search_form import ComponentSearchForm
from .components.component_result_table import ComponentResultTable


class TestFESearchBasic(TestMRTBase):
    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown_method(self, driver):
        self.driver = driver

        self.url = self.host_url + 'search_basic'
        self.driver.get(self.url)

        yield

    def test_search_basic_get(self):
        mrt_map = ComponentMRTMap(self.driver)
        assert mrt_map, 'mrt_map does not exist'

        line1 = ComponentMRTLink(self.driver, 'MacPherson(CC10)Tai Seng(CC11)CC')
        assert line1.is_activated()

    def test_search_basic_success(self):
        un_used_link = ComponentMRTLink(self.driver, 'Outram Park(EW16)Outram Park(NE3)LINE_CHANGE')
        used_link = ComponentMRTLink(self.driver, 'Farrer Road(CC20)Holland Village(CC21)CC')
        assert un_used_link.is_activated()
        assert used_link.is_activated()

        form = ComponentSearchForm(self.driver)
        form.src_name.send_keys('Holland Village')
        form.des_name.send_keys('Little India')
        form.submit.click()

        un_used_link = ComponentMRTLink(self.driver, 'Outram Park(EW16)Outram Park(NE3)LINE_CHANGE')
        used_link = ComponentMRTLink(self.driver, 'Farrer Road(CC20)Holland Village(CC21)CC')
        assert not un_used_link.is_activated()
        assert used_link.is_activated()

        message = self.driver.find_element_by_id('message')
        assert 'Total travel time is' in message.text

        table = ComponentResultTable(self.driver)
        assert table.head[0].text == 'Actions'

        body = table.body
        assert len(body) == 6
        row_0 = body[0]

        assert row_0[0].text == 'Take CC line'
        assert row_0[1].text == 'Holland Village'
        assert row_0[2].text == 'Farrer Road'

    def test_search_basic_fail(self):
        un_used_link = ComponentMRTLink(self.driver, 'Farrer Road(CC20)Holland Village(CC21)CC')
        assert un_used_link.is_activated()

        form = ComponentSearchForm(self.driver)
        form.submit.click()

        un_used_link = ComponentMRTLink(self.driver, 'Farrer Road(CC20)Holland Village(CC21)CC')
        assert not un_used_link.is_activated()

        message = self.driver.find_element_by_id('message')
        assert 'No invalid action, you can not go further or the path is blocked' in message.text

        with pytest.raises(NoSuchElementException):
            ComponentResultTable(self.driver)
