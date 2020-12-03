from abc import ABCMeta, abstractmethod
from datetime import datetime
import logging

from mrt.core.mrt_map import MRTMap
from mrt.core.mrt_schedule import MRTSchedule
from mrt.core.mrt_station import MRTStation
from mrt.core.travel_plan import TravelPlan

logger = logging.getLogger(__name__)


class ABCMRTSearchEngine(metaclass=ABCMeta):
    def __init__(self):
        self._mrt_map = MRTMap()
        self._mrt_schedule = MRTSchedule()

    @abstractmethod
    def search(self, src_station: MRTStation, des_name: str, cur_time: datetime) -> TravelPlan:
        pass

    def search_by_name(self, src_name: str, des_name: str, cur_time) -> TravelPlan:
        src_list = self.mrt_map.get_station_by_name(src_name)
        plan_list = []
        for src_station in src_list:
            plan_list.append(self.search(src_station, des_name, cur_time))

        return self.find_best_plan(plan_list)

    def find_best_plan(self, plan_list: list) -> TravelPlan:
        best_plan = TravelPlan.build_unreachable_plan()
        for plan in plan_list:
            # current best plan is unreachable
            if plan.is_better_than(best_plan):
                best_plan = plan
        return best_plan

    @property
    def mrt_map(self) -> MRTMap:
        return self._mrt_map

    @property
    def mrt_schedule(self) -> MRTSchedule:
        return self._mrt_schedule

    def init(self):
        self.mrt_map.init()
        self.mrt_schedule.init()
