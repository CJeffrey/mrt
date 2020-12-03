from datetime import timedelta
from .travel_step import TravelStep


class TravelPlan:
    def __init__(self):
        self._step_list = []

    def get_travel_station_list(self):
        return [x.des for x in self.step_list]

    def get_travel_time_in_min(self):
        if len(self.step_list) != 0:
            duration = sum([x.duration for x in self.step_list], start=timedelta())
            return duration.seconds // 60
        else:
            return None

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

    def is_better_than(self, other) -> bool:
        """
        check whether this plan is better than other, will compared by get_travel_time_in_min.
            if travel_time_in_min are equal, return False

        :param other:
        :return:
        """
        if not isinstance(other, TravelPlan):
            raise TypeError('should get a TravelPlan but got {}'.format(other))

        other_time = other.get_travel_time_in_min()
        self_time = self.get_travel_time_in_min()

        if self_time is None and other_time is None:
            return False
        elif self_time is None:
            return False
        elif other_time is None:
            return True
        else:
            return self_time < other_time
