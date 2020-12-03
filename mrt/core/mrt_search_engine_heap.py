from datetime import datetime, timedelta
from heapq import heappush, heappop

from .abc_mrt_search_engine import ABCMRTSearchEngine
from .mrt_station import MRTStation
from .travel_plan import TravelPlan
from .travel_step import TravelStep


class MRTSearchEngineHeap(ABCMRTSearchEngine):
    def search(self, src_station: MRTStation, des_name: str, cur_time: datetime) -> TravelPlan:
        heap = [TravelStep(src_station, src_station, cur_time, timedelta(), previous_step=None)]
        seen = set()

        final_step = None
        while len(heap) > 0:
            step = heappop(heap)
            next_start_station = step.des
            next_start_time = step.end_time

            if next_start_station in seen:
                continue
            seen.add(next_start_station)

            if next_start_station.open_date > step.end_time:
                # won't use an un-opened station
                continue

            if next_start_station.name == des_name:
                final_step = step
                break

            for station in next_start_station.next_stations:
                duration = self.mrt_schedule.get_travel_time(next_start_station, station, next_start_time)
                if duration is not None:
                    heappush(heap,
                             TravelStep(next_start_station, station, next_start_time, duration, previous_step=step))

        return TravelPlan.build_from_final_step(final_step)
