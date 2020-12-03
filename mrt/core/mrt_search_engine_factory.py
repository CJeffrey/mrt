from .abc_mrt_search_engine import ABCMRTSearchEngine
from .mrt_search_engine_heap import MRTSearchEngineHeap


class MRTSearchEngineFactory:
    def get_search_engine(self) -> ABCMRTSearchEngine:
        return MRTSearchEngineHeap()
