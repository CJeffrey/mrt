from datetime import datetime

from ..utils.singleton import Singleton
from .mrt_station import MRTStation
from .travel_plan import TravelPlan
from .mrt_search_engine_factory import MRTSearchEngineFactory


class MRTSolution(metaclass=Singleton):
    def __init__(self):
        self.engine_factory = MRTSearchEngineFactory()

    def search(self, src: MRTStation, des: MRTStation, cur_time: datetime) -> TravelPlan:
        engine = self.engine_factory.get_search_engine()
        return engine.search(src, des, cur_time)
