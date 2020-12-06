from datetime import datetime, timedelta

from .mrt_station import MRTStation


class TravelStep:
    TIME_FORMAT = '%Y-%m-%dT%H:%M'

    def __init__(self, src: MRTStation = None, des: MRTStation = None,
                 start_time: datetime = None, duration: timedelta = None,
                 previous_step=None) -> None:
        self._src = src
        self._des = des
        self._start_time = start_time
        self._duration = duration
        if self._start_time is None or self._duration is None:
            self._end_time = None
        else:
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
        """
        Compare by end_time

        :param other: the other TravelStep object
        :return:
        """
        if not isinstance(other, TravelStep):
            raise ValueError('Can only compare with TravelStep but got {}'.format(other))

        return self.end_time < other.end_time

    @staticmethod
    def build_invalid_step():
        """
        Build an invalid step

        :return: an invalid step
        """
        return TravelStep()

    def is_invalid_step(self) -> bool:
        """
        Check if this is an invalid step

        :return: True if this is an invalid step
        """
        return self.src is None or self.des is None

    def get_readable_action(self) -> str:
        """
        Get a readable action instruction

        :return: readable action string
        """
        if self.is_invalid_step():
            return 'No invalid action, you can not go further or the path is blocked'
        elif self.src.key == self.des.key:
            return 'No more action needed, you are already arrived'
        elif self.src.line_tag == self.des.line_tag:
            return 'Take {line_tag} line'.format(line_tag=self.src.line_tag.name)
        else:
            return 'Change from {src} line to {des} line'.format(
                src=self.src.line_tag.name,
                des=self.des.line_tag.name,
            )

    def get_readable_station_details(self) -> str:
        """
        Get readable station info details

        :return: station details
        """
        if self.is_invalid_step():
            return ''
        else:
            return 'from {src_name}({src_key}) station to {des_name}({des_key}) station'.format(
                src_name=self.src.name,
                src_key=self.src.key,
                des_name=self.des.name,
                des_key=self.des.key,
            )

    def get_readable_time_details(self) -> str:
        """
        Get readable travel time details

        :return: travel time details
        """
        if self.is_invalid_step():
            return ''
        else:
            return 'start from {start_time}, end in {end_time}, duration {duration_min} minutes'.format(
                start_time=self._start_time.strftime(self.TIME_FORMAT),
                end_time=self._end_time.strftime(self.TIME_FORMAT),
                duration_min=self._duration.seconds // 60
            )

    def get_link_info(self) -> list:
        """
        Get the link info of this step

        :return: the link info
        """
        return self.src.get_link_info_with_station(self.des)
