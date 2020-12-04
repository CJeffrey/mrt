from datetime import datetime, timedelta
from heapq import heappush, heappop

from .abc_mrt_search_engine import ABCMRTSearchEngine
from .mrt_station import MRTStation
from .travel_plan import TravelPlan
from .travel_step import TravelStep


class MRTSearchEngineHeap(ABCMRTSearchEngine):
    """
    Use Dijkstra Algorithm.
    Use a simple heap to store the unreached nodes
    """
    def search(self, src_station: MRTStation, des_name: str, cur_time: datetime) -> TravelPlan:
        """
        Use Dijkstra Algorithm and a simple heap to search

        :param src_station: the source station
        :param des_name: the destination station name
        :param cur_time: the time when start travel in src_station
        :return: the shortest travel plan
        """
        # init the heap by source station
        heap = [TravelStep(src_station, src_station, cur_time, timedelta(), previous_step=None)]
        # use a set to filter the seen stations
        seen = set()

        final_step = None
        while len(heap) > 0:
            # get the step with the minimal end_time
            step = heappop(heap)
            next_start_station = step.des
            next_start_time = step.end_time

            if next_start_station in seen:
                # already in seen then skip this station
                continue
            seen.add(next_start_station)

            if next_start_station.open_date > step.end_time:
                # won't use an un-opened station
                continue

            if next_start_station.name == des_name:
                # search ends when find the destination name
                final_step = step
                break

            for station in next_start_station.next_stations:
                if station in seen:
                    # skip the already seen next station
                    continue
                # update all the next_stations
                duration = self.mrt_schedule.get_travel_time(next_start_station, station, next_start_time)
                if duration is not None:
                    # won't try to add None duration, because None means unreachable
                    heappush(heap,
                             TravelStep(next_start_station, station, next_start_time, duration, previous_step=step))

        return TravelPlan.build_from_final_step(final_step)
