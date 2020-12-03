import pytest
from datetime import timedelta, datetime

from mrt.core.mrt_search_engine_heap import MRTSearchEngineHeap
from mrt.core.mrt_schedule import TimeDuration
from mrt.core.mrt_line_tag import LineTags

from . import get_data_file_path

ONE_MIN_SCHEDULE = TimeDuration({}, timedelta(minutes=1))
START_TIME = datetime(year=2020, month=1, day=1)
PEAK_TIME = datetime(year=2020, month=12, day=2, hour=6)
NIGHT_TIME = datetime(year=2020, month=1, day=1, hour=23)


class TestMRTSearchEngineHeap:
    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown_method(self):
        self.engine = MRTSearchEngineHeap()
        self.engine.init()
        yield

    @pytest.fixture(scope='function')
    def test_data_1(self):
        self.engine.mrt_schedule.init(
            peak_schedule=ONE_MIN_SCHEDULE, night_schedule=ONE_MIN_SCHEDULE, ordinary_schedule=ONE_MIN_SCHEDULE)
        self.engine.mrt_map.init(get_data_file_path('engine1.csv'))
        yield

    def test_two_stations(self, test_data_1):
        ns1 = self.engine.mrt_map.get_station_by_key('NS1')
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')

        plan = self.engine.search(ns1, ns2, START_TIME)
        station_list = plan.get_travel_station_list()

        assert len(station_list) == 2
        assert station_list[0] == ns1
        assert station_list[1] == ns2

        assert plan.get_travel_time_in_min() == 1

    def test_single_station(self, test_data_1):
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')

        plan = self.engine.search(ns2, ns2, START_TIME)
        station_list = plan.get_travel_station_list()

        assert len(station_list) == 1
        assert station_list[0] == ns2

        assert plan.get_travel_time_in_min() == 0

    def test_unreachable_station(self, test_data_1):
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')
        dt3 = self.engine.mrt_map.get_station_by_key('DT3')

        plan = self.engine.search(ns2, dt3, START_TIME)
        station_list = plan.get_travel_station_list()

        assert len(station_list) == 0
        assert plan.get_travel_time_in_min() is None

    def test_un_opened_station(self, test_data_1):
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')
        ns3 = self.engine.mrt_map.get_station_by_key('NS3')

        # station ns3 does not open yet
        plan = self.engine.search(ns2, ns3, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0
        assert plan.get_travel_time_in_min() is None

        # station ns3 will open on the next day
        plan = self.engine.search(ns2, ns3, START_TIME + timedelta(days=1))
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 2

    def test_cross_un_opened_station(self, test_data_1):
        ns1 = self.engine.mrt_map.get_station_by_key('NS1')
        ns4 = self.engine.mrt_map.get_station_by_key('NS4')

        plan = self.engine.search(ns1, ns4, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0

    def test_half_open_station(self, test_data_1):
        ns6 = self.engine.mrt_map.get_station_by_key('NS6')
        ns5 = self.engine.mrt_map.get_station_by_key('NS5')
        ew5 = self.engine.mrt_map.get_station_by_key('EW5')

        plan = self.engine.search(ns6, ns5, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 2

        plan = self.engine.search(ns6, ew5, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0

        plan = self.engine.search(ns6, ew5, START_TIME + timedelta(days=1))
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 3

    def test_nightly_stopped_station(self):
        # make NE to stop at night time
        self.engine.mrt_schedule.init(
            peak_schedule=ONE_MIN_SCHEDULE,
            night_schedule=TimeDuration({
                LineTags['NE']: None,
            }, timedelta(minutes=1)),
            ordinary_schedule=ONE_MIN_SCHEDULE)
        self.engine.mrt_map.init(get_data_file_path('engine1.csv'))

        ns6 = self.engine.mrt_map.get_station_by_key('NS7')
        ns7 = self.engine.mrt_map.get_station_by_key('NS7')
        ne7 = self.engine.mrt_map.get_station_by_key('NE7')
        ne8 = self.engine.mrt_map.get_station_by_key('NE8')

        # you can go to ns7 because ns is open
        plan = self.engine.search(ns6, ns7, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 1

        # you can go from ns7 to ne7 although ne is closed,
        plan = self.engine.search(ns7, ne7, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 2

        # you can go from ns7 to ne7 although ne is closed,
        plan = self.engine.search(ne7, ns7, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 2

        # you can not go from ns7 to ne8, because ne is closed
        plan = self.engine.search(ns7, ne8, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0

        # you can go from ns7 to ne8 in peak time
        plan = self.engine.search(ns7, ne8, PEAK_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 3

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
