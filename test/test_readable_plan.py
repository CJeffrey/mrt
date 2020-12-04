from datetime import datetime, timedelta

from mrt.core.travel_plan import TravelPlan
from mrt.core.mrt_station import MRTStation
from mrt.core.travel_step import TravelStep


class TestReadablePlan:
    def test_unreachable_plan(self):
        """
        Test the behavior of an unreachable plan
        """
        travel_plan_unreachable = TravelPlan.build_unreachable_plan()
        readable_plan = travel_plan_unreachable.get_readable_plan()

        assert not readable_plan.is_reachable()
        assert readable_plan.message == 'No invalid action, you can not go further or the path is blocked'
        assert len(readable_plan.step_list) == 1
        step0 = readable_plan.step_list[0]
        assert step0.get_readable_action() == 'No invalid action, you can not go further or the path is blocked'

    def test_already_arrived(self):
        """
        Test the behavior when you already arrived the station before travel
        """
        time = datetime(year=2000, month=1, day=1)
        s1 = MRTStation('NS1', '', time)
        travel_step_1 = TravelStep(s1, s1, time, duration=timedelta())

        travel_plan_1 = TravelPlan.build_from_final_step(travel_step_1)
        readable_plan = travel_plan_1.get_readable_plan()

        assert readable_plan.is_reachable()
        assert readable_plan.message == 'Total travel time is 0 minutes'
        assert len(readable_plan.step_list) == 1
        step0 = readable_plan.step_list[0]
        assert step0.get_readable_action() == 'No more action needed, you are already arrived'

    def test_only_change_station(self):
        """
        Only change the station, no taking
        """
        time = datetime(year=2000, month=1, day=1)
        ns1 = MRTStation('NS1', 'NAME1', time)
        dt1 = MRTStation('DT1', 'NAME1', time)
        travel_step_1 = TravelStep(ns1, ns1, time, duration=timedelta())
        travel_step_2 = TravelStep(ns1, dt1, time, duration=timedelta(minutes=7))

        travel_plan = TravelPlan()
        travel_plan.step_list.append(travel_step_1)
        travel_plan.step_list.append(travel_step_2)

        readable_plan = travel_plan.get_readable_plan()

        assert readable_plan.is_reachable()
        assert readable_plan.message == 'Total travel time is 7 minutes'
        assert len(readable_plan.step_list) == 1
        step0 = readable_plan.step_list[0]
        assert step0.get_readable_action() == 'Change from NS line to DT line'

    def test_only_take_station(self):
        """
        Only take the station, no change
        """
        time = datetime(year=2000, month=1, day=1)
        ns1 = MRTStation('NS1', 'NAME1', time)
        ns2 = MRTStation('NS2', 'NAME1', time)
        travel_step_1 = TravelStep(ns1, ns1, time, duration=timedelta())
        travel_step_2 = TravelStep(ns1, ns2, time, duration=timedelta(minutes=6))

        travel_plan = TravelPlan()
        travel_plan.step_list.append(travel_step_1)
        travel_plan.step_list.append(travel_step_2)

        readable_plan = travel_plan.get_readable_plan()

        assert readable_plan.is_reachable()
        assert readable_plan.message == 'Total travel time is 6 minutes'
        assert len(readable_plan.step_list) == 1
        step0 = readable_plan.step_list[0]
        assert step0.get_readable_action() == 'Take NS line'
