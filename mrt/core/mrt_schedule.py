import copy
from datetime import datetime, timedelta
from enum import Enum
import logging

from ..utils.singleton import Singleton
from .mrt_station import MRTStation
from .mrt_line_tag import LineTags
from .exceptions import InvalidTransportError

logger = logging.getLogger(__name__)


class TimeDuration:
    def __init__(self, data: dict, default_cost: timedelta) -> None:
        self.data = copy.copy(data)
        self.default_cost = default_cost

    def get_time_duration(self, line_tag: LineTags) -> timedelta:
        return self.data.get(line_tag, self.default_cost)


HourTypes = Enum(
    'HourTypes',
    ('Peak', 'Night', 'Ordinary')
)


class MRTSchedule(metaclass=Singleton):
    def __init__(self):
        self.schedules = None
        self.init()

    def init(self, peak_schedule=None, night_schedule=None, ordinary_schedule=None):
        logger.info('init MRTSchedule schedules')

        if peak_schedule is None:
            peak_schedule = TimeDuration({
                LineTags.NS: timedelta(minutes=12),
                LineTags.NE: timedelta(minutes=12),
                LineTags.LINE_CHANGE: timedelta(minutes=15),
            }, timedelta(minutes=10))

        if night_schedule is None:
            night_schedule = TimeDuration({
                LineTags.DT: None,
                LineTags.CG: None,
                LineTags.CE: None,
                LineTags.TE: timedelta(minutes=8),
                LineTags.LINE_CHANGE: timedelta(minutes=10),
            }, timedelta(minutes=10))

        if ordinary_schedule is None:
            ordinary_schedule = TimeDuration({
                LineTags.DT: timedelta(minutes=8),
                LineTags.TE: timedelta(minutes=8),
                LineTags.LINE_CHANGE: timedelta(minutes=10),
            }, timedelta(minutes=10))

        self.schedules = {
            HourTypes.Peak: peak_schedule,
            HourTypes.Night: night_schedule,
            HourTypes.Ordinary: ordinary_schedule,
        }

    def get_hour_type(self, time: datetime) -> HourTypes:
        if self.is_peak_hour(time):
            return HourTypes.Peak
        elif self.is_night_hour(time):
            return HourTypes.Night
        else:
            return HourTypes.Ordinary

    def get_travel_time(self, src: MRTStation, des: MRTStation, cur_time: datetime) -> timedelta:
        if src.key == des.key:
            raise InvalidTransportError('can not transfer in the same station {} to {}'.format(src, des))
        if des not in src.next_stations:
            raise InvalidTransportError('can not transfer in unconnected stations {} to {}'.format(src, des))

        if src.line_tag == des.line_tag:
            line_tag = src.line_tag
        elif src.name == des.name:
            line_tag = LineTags.LINE_CHANGE
        else:
            raise InvalidTransportError('can not transfer from {} to {}'.format(src, des))

        hour_type = self.get_hour_type(cur_time)
        return self.schedules[hour_type].get_time_duration(line_tag)

    def is_peak_hour(self, time: datetime) -> bool:
        return 0 <= time.weekday() <= 4 and (6 <= time.hour < 9 or 18 <= time.hour < 21)

    def is_night_hour(self, time: datetime) -> bool:
        return time.hour >= 22 or time.hour < 6

    def is_ordinary_hour(self, time: datetime) -> bool:
        return not (self.is_peak_hour(time) or self.is_night_hour(time))
