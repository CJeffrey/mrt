from datetime import datetime, timedelta

from .mrt_station import MRTStation


class TravelStep:
    def __init__(self, src: MRTStation, des: MRTStation, start_time: datetime, duration: timedelta,
                 previous_step=None) -> None:
        self._src = src
        self._des = des
        self._start_time = start_time
        self._duration = duration
        self._end_time = start_time + duration
        self._previous_step = previous_step

    @property
    def src(self) -> MRTStation:
        return self._src

    @property
    def des(self) -> MRTStation:
        return self._des

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @property
    def duration(self) -> timedelta:
        return self._duration

    @property
    def previous_step(self):
        return self._previous_step

    def __lt__(self, other):
        if not isinstance(other, TravelStep):
            raise ValueError('Can only compare with TravelStep but got {}'.format(other))

        return self.end_time < other.end_time
