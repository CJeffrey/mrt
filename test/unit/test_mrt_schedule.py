import pytest
from datetime import datetime, timedelta
from mrt.core.mrt_schedule import MRTSchedule
from mrt.core.mrt_station import MRTStation


class TestMRTSchedule:
    DELTA_1_SECOND = timedelta(seconds=1)

    @pytest.fixture(scope='function', autouse=True)
    def setup_teardown_method(self):
        self.mrt_schedule = MRTSchedule()
        yield

    def test_is_peak_hour(self):
        """
        Test the peak hour behavior
        """
        monday_6 = datetime(year=2020, month=11, day=30, hour=6, minute=0, second=0)
        monday_9 = datetime(year=2020, month=11, day=30, hour=9, minute=0, second=0)
        monday_18 = datetime(year=2020, month=11, day=30, hour=18, minute=0, second=0)
        monday_21 = datetime(year=2020, month=11, day=30, hour=21, minute=0, second=0)

        for delta_day_int in range(5):
            delta_day = timedelta(days=delta_day_int)
            assert self.mrt_schedule.is_peak_hour(monday_6 + delta_day)
            assert not self.mrt_schedule.is_peak_hour(monday_6 + delta_day - self.DELTA_1_SECOND)
            assert not self.mrt_schedule.is_peak_hour(monday_9 + delta_day)
            assert self.mrt_schedule.is_ordinary_hour(monday_9 + delta_day)
            assert self.mrt_schedule.is_peak_hour(monday_9 + delta_day - self.DELTA_1_SECOND)

            assert self.mrt_schedule.is_peak_hour(monday_18 + delta_day)
            assert not self.mrt_schedule.is_peak_hour(monday_18 + delta_day - self.DELTA_1_SECOND)
            assert self.mrt_schedule.is_ordinary_hour(monday_18 + delta_day - self.DELTA_1_SECOND)
            assert not self.mrt_schedule.is_peak_hour(monday_21 + delta_day)
            assert self.mrt_schedule.is_ordinary_hour(monday_21 + delta_day)
            assert self.mrt_schedule.is_peak_hour(monday_21 + delta_day - self.DELTA_1_SECOND)

        for delta_day_int in range(5, 7):
            delta_day = timedelta(days=delta_day_int)
            assert not self.mrt_schedule.is_peak_hour(monday_6 + delta_day)
            assert self.mrt_schedule.is_ordinary_hour(monday_6 + delta_day)
            assert not self.mrt_schedule.is_peak_hour(monday_6 + delta_day - self.DELTA_1_SECOND)
            assert not self.mrt_schedule.is_peak_hour(monday_9 + delta_day)
            assert self.mrt_schedule.is_ordinary_hour(monday_9 + delta_day)
            assert not self.mrt_schedule.is_peak_hour(monday_9 + delta_day - self.DELTA_1_SECOND)
            assert self.mrt_schedule.is_ordinary_hour(monday_9 + delta_day - self.DELTA_1_SECOND)

            assert not self.mrt_schedule.is_peak_hour(monday_18 + delta_day)
            assert self.mrt_schedule.is_ordinary_hour(monday_18 + delta_day)
            assert not self.mrt_schedule.is_peak_hour(monday_18 + delta_day - self.DELTA_1_SECOND)
            assert self.mrt_schedule.is_ordinary_hour(monday_18 + delta_day - self.DELTA_1_SECOND)
            assert not self.mrt_schedule.is_peak_hour(monday_21 + delta_day)
            assert self.mrt_schedule.is_ordinary_hour(monday_21 + delta_day)
            assert not self.mrt_schedule.is_peak_hour(monday_21 + delta_day - self.DELTA_1_SECOND)
            assert self.mrt_schedule.is_ordinary_hour(monday_21 + delta_day - self.DELTA_1_SECOND)

    def test_is_night_hour(self):
        """
        Test the night hour behavior
        """
        monday_6 = datetime(year=2020, month=11, day=30, hour=6, minute=0, second=0)
        monday_22 = datetime(year=2020, month=11, day=30, hour=22, minute=0, second=0)

        for delta_day_int in range(7):
            delta_day = timedelta(days=delta_day_int)

            assert self.mrt_schedule.is_night_hour(monday_22 + delta_day)
            assert not self.mrt_schedule.is_night_hour(monday_22 + delta_day - self.DELTA_1_SECOND)
            assert self.mrt_schedule.is_ordinary_hour(monday_22 + delta_day - self.DELTA_1_SECOND)
            assert not self.mrt_schedule.is_night_hour(monday_6 + delta_day)
            assert self.mrt_schedule.is_night_hour(monday_6 + delta_day - self.DELTA_1_SECOND)

    def test_get_travel_time(self):
        """
        Test the get travel time behavior
        """
        sample_peak_hour = datetime(year=2020, month=11, day=30, hour=7, minute=0, second=0)
        sample_night_hour = datetime(year=2020, month=11, day=30, hour=0, minute=0, second=0)
        sample_ordinary_hour = datetime(year=2020, month=11, day=30, hour=13, minute=0, second=0)

        dt1 = MRTStation('DT1', 'Station1', datetime.now())
        dt2 = MRTStation('DT2', 'Station2', datetime.now())
        ne1 = MRTStation('NE1', 'Station2', datetime.now())

        dt1.add_next_station(dt2)
        dt2.add_next_station(dt1)
        dt2.add_next_station(ne1)
        ne1.add_next_station(dt2)

        assert self.mrt_schedule.get_travel_time(dt1, dt2, sample_peak_hour) == timedelta(minutes=10)
        assert self.mrt_schedule.get_travel_time(dt1, dt2, sample_night_hour) is None
        assert self.mrt_schedule.get_travel_time(dt1, dt2, sample_ordinary_hour) == timedelta(minutes=8)

        assert self.mrt_schedule.get_travel_time(dt2, ne1, sample_peak_hour) == timedelta(minutes=15)
        assert self.mrt_schedule.get_travel_time(ne1, dt2, sample_ordinary_hour) == timedelta(minutes=10)
        assert self.mrt_schedule.get_travel_time(dt2, ne1, sample_ordinary_hour) == timedelta(minutes=10)
