import pytest
from datetime import timedelta, datetime

from mrt.core.mrt_search_engine_heap import MRTSearchEngineHeap
from mrt.core.mrt_schedule import TimeDuration

from . import get_data_file_path

ONE_MIN_SCHEDULE = TimeDuration({}, timedelta(minutes=1))
START_TIME = datetime(year=2020, month=1, day=1)
PEAK_TIME = datetime(year=2020, month=12, day=2, hour=6)


class TestMRTSearchEngineHeap:
    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown_method(self):
        self.engine = MRTSearchEngineHeap()
        self.engine.init()
        yield

    def test_two_stations(self):
        self.engine.mrt_schedule.init(
            peak_schedule=ONE_MIN_SCHEDULE, night_schedule=ONE_MIN_SCHEDULE, ordinary_schedule=ONE_MIN_SCHEDULE)
        self.engine.mrt_map.init(get_data_file_path('engine1.csv'))

        s1 = self.engine.mrt_map.get_station_by_key('NS1')
        s2 = self.engine.mrt_map.get_station_by_key('NS2')

        plan = self.engine.search(s1, s2, START_TIME)
        station_list = plan.get_travel_station_list()

        assert len(station_list) == 2
        assert station_list[0] == s1
        assert station_list[1] == s2

        assert plan.get_travel_time_in_min() == 1

    def test_real(self):
        cc21 = self.engine.mrt_map.get_station_by_key('CC21')
        ew12 = self.engine.mrt_map.get_station_by_key('DT14')

        plan = self.engine.search(cc21, ew12, PEAK_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 9

        ew27 = self.engine.mrt_map.get_station_by_key('EW27')
        dt12 = self.engine.mrt_map.get_station_by_key('DT12')

        plan = self.engine.search(ew27, dt12, PEAK_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 15
        travel_time = plan.get_travel_time_in_min()
        assert travel_time == 150
