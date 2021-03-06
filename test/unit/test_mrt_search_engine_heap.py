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


def gen_fixture(file_name):
    """
    Generate fixture to ingest test map data

    :param file_name: the test map data
    :return: the fixture
    """
    @pytest.fixture(scope='function')
    def _test_fixture(self, *args, **kwargs):
        self.engine.mrt_schedule.init(
            peak_schedule=ONE_MIN_SCHEDULE, night_schedule=ONE_MIN_SCHEDULE, ordinary_schedule=ONE_MIN_SCHEDULE)
        self.engine.mrt_map.init(get_data_file_path(file_name))
        yield
    return _test_fixture


class TestMRTSearchEngineHeap:
    # engine1.csv
    # NS1<->NS2<->NS3<->NS4<->NS5<->NS6<->NS7
    #                          |           |       DT3(Single)
    #                         EW5<->EW6    |
    #                                     NE7<->NE8
    test_data_1 = gen_fixture('engine1.csv')

    # engine2.csv
    # NS1<->NS2<->NS3<->NS4<->NS5<->NS6<->NS7
    #                                |
    #                               EW6<->EW7
    test_data_2 = gen_fixture('engine2.csv')

    # engine3.csv
    # NS1<->NS2<->NS3<->NS4<->NS5<->NS6<->NS7
    #        |                       |
    #       DT2         <->         DT3
    test_data_3 = gen_fixture('engine3.csv')

    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown_method(self):
        self.engine = MRTSearchEngineHeap()
        self.engine.init()
        yield

    def test_two_stations(self, test_data_1):
        """
        Test travel in only two stations
        """
        ns1 = self.engine.mrt_map.get_station_by_key('NS1')
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')

        plan = self.engine.search(ns1, ns2.name, START_TIME)
        station_list = plan.get_travel_station_list()

        assert len(station_list) == 2
        assert station_list[0] == ns1
        assert station_list[1] == ns2

        assert plan.get_travel_time_in_min() == 1

    def test_single_station(self, test_data_1):
        """
        Test travel in the same station
        """
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')

        plan = self.engine.search(ns2, ns2.name, START_TIME)
        station_list = plan.get_travel_station_list()

        assert len(station_list) == 1
        assert station_list[0] == ns2

        assert plan.get_travel_time_in_min() == 0

    def test_unreachable_station(self, test_data_1):
        """
        Test a station which is un reachable
        """
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')
        dt3 = self.engine.mrt_map.get_station_by_key('DT3')

        plan = self.engine.search(ns2, dt3.name, START_TIME)
        station_list = plan.get_travel_station_list()

        assert len(station_list) == 0
        assert plan.get_travel_time_in_min() is None

    def test_un_opened_station(self, test_data_1):
        """
        Test travel to station which is not opened
        """
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')
        ns3 = self.engine.mrt_map.get_station_by_key('NS3')

        # station ns3 does not open yet
        plan = self.engine.search(ns2, ns3.name, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0
        assert plan.get_travel_time_in_min() is None

        # station ns3 will open on the next day
        plan = self.engine.search(ns2, ns3.name, START_TIME + timedelta(days=1))
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 2

    def test_just_opened_station(self, test_data_1):
        """
        When starting the journey, the station is not opened yet. But it opens during the journey.
        """
        ns2 = self.engine.mrt_map.get_station_by_key('NS2')
        ns3 = self.engine.mrt_map.get_station_by_key('NS3')

        # station ns3 does not open yet
        travel_time = datetime(year=2020, month=1, day=2) - timedelta(seconds=30)
        plan = self.engine.search(ns2, ns3.name, travel_time)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 2

        step_list = plan.step_list
        assert step_list[1].start_time < ns3.open_date
        assert step_list[1].end_time > ns3.open_date

    def test_cross_un_opened_station(self, test_data_1):
        """
        Try to cross an unopened station
        """
        ns1 = self.engine.mrt_map.get_station_by_key('NS1')
        ns4 = self.engine.mrt_map.get_station_by_key('NS4')

        plan = self.engine.search(ns1, ns4.name, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0

    def test_half_open_station(self, test_data_1):
        """
        ns6<->ns5, ns5==ew5, ew5<->ew6
        ew5 is not open on START_TIME, but will open in next day

        """
        ns6 = self.engine.mrt_map.get_station_by_key('NS6')
        ns5 = self.engine.mrt_map.get_station_by_key('NS5')
        ew5 = self.engine.mrt_map.get_station_by_key('EW5')
        ew6 = self.engine.mrt_map.get_station_by_key('EW6')

        # we can go from ns6 to ns5, because ns5 is opened
        plan = self.engine.search(ns6, ns5.name, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 2

        # we can't go from ns6 to ew6, because we5 is closed
        plan = self.engine.search(ns6, ew6.name, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0

        # we can't go from ew6 to ew5, because ew5 is closed
        plan = self.engine.search(ew6, ew5.name, START_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0

        # we can go from ns6 to ew6 in the next day
        plan = self.engine.search(ns6, ew6.name, START_TIME + timedelta(days=1))
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 4

    def test_nightly_stopped_station(self):
        """
        ns6<->ns7, ns7==ne7, ne7<->ne8
        ne is closed in night time

        """
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
        plan = self.engine.search(ns6, ns7.name, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 1

        # you can go from ns7 to ne7 although ne is closed,
        plan = self.engine.search(ns7, ne7.name, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 1

        # you can go from ns7 to ne7 although ne is closed,
        plan = self.engine.search(ne7, ns7.name, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 1

        # you can not go from ns7 to ne8, because ne is closed
        plan = self.engine.search(ns7, ne8.name, NIGHT_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 0

        # you can go from ns7 to ne8 in peak time
        plan = self.engine.search(ns7, ne8.name, PEAK_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 3

    def test_real(self):
        """
        Test on a real map
        """
        cc21 = self.engine.mrt_map.get_station_by_key('CC21')
        ew12 = self.engine.mrt_map.get_station_by_key('DT14')

        plan = self.engine.search(cc21, ew12.name, PEAK_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 9

        ew27 = self.engine.mrt_map.get_station_by_key('EW27')
        dt12 = self.engine.mrt_map.get_station_by_key('DT12')

        plan = self.engine.search(ew27, dt12.name, PEAK_TIME)
        station_list = plan.get_travel_station_list()
        assert len(station_list) == 15
        travel_time = plan.get_travel_time_in_min()
        assert travel_time == 150

    def test_search_by_name(self, test_data_2):
        """
        Test search by name, but not station object
        :return:
        """
        plan = self.engine.search_by_name('NS1', 'NS7', START_TIME)
        assert len(plan.get_travel_station_list()) == 7
        assert plan.get_travel_time_in_min() == 6

        plan = self.engine.search_by_name('NS1', 'NS6', START_TIME)
        assert len(plan.get_travel_station_list()) == 6

        plan = self.engine.search_by_name('NS6', 'NS1', START_TIME)
        assert len(plan.get_travel_station_list()) == 6

        plan = self.engine.search_by_name('EW7', 'NS1', START_TIME)
        assert len(plan.get_travel_station_list()) == 8

        plan = self.engine.search_by_name('NS1', 'EW7', START_TIME)
        assert len(plan.get_travel_station_list()) == 8

    def test_circle(self, test_data_3):
        """
        Test in a circle data
        """
        ns1 = self.engine.mrt_map.key2station['NS1']
        dt3 = self.engine.mrt_map.key2station['DT3']
        ns6 = self.engine.mrt_map.key2station['NS6']

        # at first, all lines have the same speed
        plan = self.engine.search(ns1, dt3.name, START_TIME)
        assert len(plan.get_travel_station_list()) == 4
        assert plan.get_travel_station_list()[-1] == dt3

        # let's make DT very slow
        for _, val in self.engine.mrt_schedule.schedules.items():
            val.update_time_duration(LineTags.DT, timedelta(minutes=60))
        plan = self.engine.search(ns1, dt3.name, START_TIME)
        assert len(plan.get_travel_station_list()) == 6
        assert plan.get_travel_station_list()[-1] == ns6
