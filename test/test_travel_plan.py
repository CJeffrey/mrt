from datetime import timedelta, datetime

from mrt.core.travel_plan import TravelPlan
from mrt.core.travel_step import TravelStep
from mrt.core.mrt_station import MRTStation


class TestTravelPlan:
    def test_unreachable_plan(self):
        travel_step_unreachable = TravelPlan.build_unreachable_plan()
        assert len(travel_step_unreachable.get_travel_station_list()) == 0
        assert travel_step_unreachable.get_travel_time_in_min() is None

    def test_is_better_than(self):
        dummy_datetime = datetime(year=2000, month=1, day=1)
        dummy_station = MRTStation('NS1', '', dummy_datetime)
        travel_step_1 = TravelStep(dummy_station, dummy_station, dummy_datetime, duration=timedelta(minutes=1))
        travel_step_2 = TravelStep(dummy_station, dummy_station, dummy_datetime, duration=timedelta(minutes=2))

        travel_step_unreachable = TravelPlan.build_unreachable_plan()
        travel_plan_1 = TravelPlan.build_from_final_step(travel_step_1)
        travel_plan_2 = TravelPlan.build_from_final_step(travel_step_2)

        assert not travel_step_unreachable.is_better_than(travel_plan_1)
        assert travel_plan_1.is_better_than(travel_step_unreachable)

        assert travel_plan_1.is_better_than(travel_plan_2)
        assert not travel_plan_2.is_better_than(travel_plan_1)
