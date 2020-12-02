from abc import ABCMeta, abstractmethod
from datetime import datetime

from mrt.core.mrt_map import MRTMap
from mrt.core.mrt_schedule import MRTSchedule
from mrt.core.mrt_station import MRTStation
from mrt.core.travel_plan import TravelPlan


class ABCMRTSearchEngine(metaclass=ABCMeta):
    def __init__(self):
        self._mrt_map = MRTMap()
        self._mrt_schedule = MRTSchedule()

    @abstractmethod
    def search(self, src: MRTStation, des: MRTStation, cur_time: datetime) -> TravelPlan:
        pass

    @property
    def mrt_map(self) -> MRTMap:
        return self._mrt_map

    @property
    def mrt_schedule(self) -> MRTSchedule:
        return self._mrt_schedule

    def init(self):
        self.mrt_map.init()
        self.mrt_schedule.init()
