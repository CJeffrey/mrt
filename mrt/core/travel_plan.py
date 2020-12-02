from datetime import timedelta
from .travel_step import TravelStep


class TravelPlan:
    def __init__(self):
        self._step_list = []

    def get_travel_station_list(self):
        return [x.des for x in self.step_list]

    def get_travel_time_in_min(self) -> int:
        duration = sum([x.duration for x in self.step_list], start=timedelta())
        return duration.seconds // 60

    @staticmethod
    def build_unreachable_plan():
        return TravelPlan()

    @staticmethod
    def build_from_final_step(final_step: TravelStep):
        if final_step is None:
            return TravelPlan.build_unreachable_plan()

        res = TravelPlan()
        step = final_step
        while step is not None:
            res.step_list.append(step)
            step = step.previous_step
        res.step_list.reverse()
        return res

    @property
    def step_list(self):
        return self._step_list
