from datetime import datetime

from ..utils.singleton import Singleton
from .travel_plan import TravelPlan
from .mrt_search_engine_factory import MRTSearchEngineFactory


class MRTSolution(metaclass=Singleton):
    def __init__(self):
        self.engine_factory = MRTSearchEngineFactory()

    def search_by_name(self, src: str, des: str, cur_time: datetime) -> TravelPlan:
        engine = self.engine_factory.get_search_engine()
        return engine.search_by_name(src, des, cur_time)
