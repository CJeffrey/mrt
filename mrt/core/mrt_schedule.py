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
    """
    Get different time duration for different Lines
    """
    def __init__(self, data: dict, default_cost: timedelta) -> None:
        """
        Set None in the data value for representing unreachable

        :param data: key should be LineTags, value should be a timedelta
        :param default_cost: return this value if no key is matched
        """
        self.data = copy.copy(data)
        self.default_cost = default_cost

    def get_time_duration(self, line_tag: LineTags) -> timedelta:
        """
        return default_cost if not matched

        :param line_tag: the querying LineTag
        :return: time duration
        """
        return self.data.get(line_tag, self.default_cost)


# Different hour types
HourTypes = Enum(
    'HourTypes',
    ('Peak', 'Night', 'Ordinary')
)


class MRTSchedule(metaclass=Singleton):
    """
    This is a Singleton Class.
    A schedule of MRT. Could get different duration for different time/LineTag
    """
    def __init__(self):
        """
        init the schedules value
        """
        self.schedules = None
        self.init()

    def init(self, peak_schedule=None, night_schedule=None, ordinary_schedule=None):
        """
        Init the schedules object in this class.
        TODO: try to init from configure file

        :param peak_schedule: the schedule for peak hour
        :param night_schedule: the schedule for night hour
        :param ordinary_schedule: the schedule for ordinary hour
        :return:
        """
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
        """
        Get the HourType by the datetime object

        :param time: the querying time
        :return: the corresponding HourType
        """
        if self.is_peak_hour(time):
            return HourTypes.Peak
        elif self.is_night_hour(time):
            return HourTypes.Night
        else:
            return HourTypes.Ordinary

    def get_travel_time(self, src: MRTStation, des: MRTStation, cur_time: datetime) -> timedelta:
        """
        Get the travel time between two stations
        Will raise InvalidTransportError if:
            * src and des are the same Station (have the same key)
            * src and des are not in the other's next_station (they are not connected directly)
            * src and des are not in the same line, and are not the same station (have the same name)

        :param src: the source MRTStation object
        :param des: the destination MRTStation object
        :param cur_time: the datetime when travelling from source MRTStation
        :return: the needed timedelta
        """
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

    @staticmethod
    def is_peak_hour(time: datetime) -> bool:
        """
        Peak hours (6am-9am and 6pm-9pm on Mon-Fri)

        :param time: the querying time
        :return: the querying result
        """
        return 0 <= time.weekday() <= 4 and (6 <= time.hour < 9 or 18 <= time.hour < 21)

    @staticmethod
    def is_night_hour(time: datetime) -> bool:
        """
        Night hours (10pm-6am on Mon-Sun)

        :param time: the querying time
        :return: the querying result
        """
        return time.hour >= 22 or time.hour < 6

    @staticmethod
    def is_ordinary_hour(time: datetime) -> bool:
        """
        Other time than peak/night

        :param time: the querying time
        :return: the querying result
        """
        return not (MRTSchedule.is_peak_hour(time) or MRTSchedule.is_night_hour(time))
