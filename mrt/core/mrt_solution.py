from datetime import datetime

from ..utils.singleton import Singleton
from .travel_plan import TravelPlan
from .mrt_search_engine_factory import MRTSearchEngineFactory


class MRTSolution(metaclass=Singleton):
    """
    This is a Singleton Class.
    The Main class for mrt.core
    """
    def __init__(self):
        """
        init the engine factory
        """
        self.engine_factory = MRTSearchEngineFactory()

    def search_by_name(self, src: str, des: str, cur_time: datetime) -> TravelPlan:
        """
        TODO: introduce more engine

        :param src: the source station name
        :param des: the destination station name
        :param cur_time: the start travel time
        :return: the best TravelPlan
        """
        engine = self.engine_factory.get_search_engine()
        return engine.search_by_name(src, des, cur_time)
