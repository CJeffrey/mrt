from abc import ABCMeta, abstractmethod
from datetime import datetime
import logging

from mrt.core.mrt_map import MRTMap
from mrt.core.mrt_schedule import MRTSchedule
from mrt.core.mrt_station import MRTStation
from mrt.core.travel_plan import TravelPlan

logger = logging.getLogger(__name__)


class ABCMRTSearchEngine(metaclass=ABCMeta):
    """
    Abstract class for search engine
    """

    def __init__(self):
        """
        init mrt_map, mrt_schedule
        """
        self._mrt_map = MRTMap()
        self._mrt_schedule = MRTSchedule()

    @abstractmethod
    def search(self, src_station: MRTStation, des_name: str, cur_time: datetime) -> TravelPlan:
        """
        Search from a station to a destination station name

        :param src_station: the source station
        :param des_name: the destination station name
        :param cur_time: the time when start travel in src_station
        :return: the shortest travel plan
        """
        pass

    def search_by_name(self, src_name: str, des_name: str, cur_time: datetime) -> TravelPlan:
        """
        Search from a station to a destination station name
        Caution that the outcome for name to name may not be unique, we will pick the shortest one

        :param src_name: the source station name
        :param des_name: the destination station name
        :param cur_time: the time when start travel in src_station
        :return: the shortest travel plan
        """
        if not src_name or not des_name:
            return TravelPlan.build_empty_station_plan()
        elif src_name not in self.mrt_map.name2station or des_name not in self.mrt_map.name2station:
            return TravelPlan.build_invalid_station_plan()

        src_list = self.mrt_map.get_station_by_name(src_name)
        plan_list = []
        for src_station in src_list:
            plan_list.append(self.search(src_station, des_name, cur_time))

        return self.find_best_plan(plan_list)

    @staticmethod
    def find_best_plan(plan_list: list) -> TravelPlan:
        """
        Find the best travel plan.

        :param plan_list: list of TravelPlan
        :return: the best plan
        """
        # current best plan is unreachable
        best_plan = TravelPlan.build_unreachable_plan()
        for plan in plan_list:
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
