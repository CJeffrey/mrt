from .abc_mrt_search_engine import ABCMRTSearchEngine
from .mrt_search_engine_heap import MRTSearchEngineHeap


class MRTSearchEngineFactory:
    """
    Factory to return ABCMRTSearchEngine object
    """

    def get_search_engine(self) -> ABCMRTSearchEngine:
        """
        return a search engine object

        :return: ABCMRTSearchEngine object
        """
        return MRTSearchEngineHeap()
