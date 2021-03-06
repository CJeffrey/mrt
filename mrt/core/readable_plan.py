from .readable_step import ReadableStep
from .travel_step import TravelStep


class ReadablePlan:
    TIME_FORMAT = TravelStep.TIME_FORMAT
    """
    This is a ReadablePlan for human read
    """

    def __init__(self):
        """
        _step_list store the objects of TravelStep
        """
        self._step_list = []
        self._total_time_in_min = None
        self._message = ''

    @property
    def step_list(self) -> list:
        return self._step_list

    @property
    def total_time_in_min(self):
        return self._total_time_in_min

    @total_time_in_min.setter
    def total_time_in_min(self, value):
        self._total_time_in_min = value

    def is_reachable(self):
        if len(self.step_list) == 0:
            return False
        elif len(self.step_list) == 1:
            only_step = self.step_list[0]
            return not only_step.is_invalid_step()
        else:
            return True

    def get_readable_outcome(self) -> list:
        """
        Get a readable outcome

        :return: a list of ReadableStep
        """
        out_come = []

        for step in self.step_list:
            single_outcome = ReadableStep(
                action=step.get_readable_action(),
                station_details=step.get_readable_station_details(),
                time_details=step.get_readable_time_details(),
                src_station=step.src.name,
                des_station=step.des.name,
                src_time=step.start_time.strftime(self.TIME_FORMAT),
                des_time=step.end_time.strftime(self.TIME_FORMAT),
                duration=step.duration,
            )
            out_come.append(single_outcome)

        return out_come

    def get_special_color_list(self) -> list:
        """
        Get the special color link list
        :return: the special color list
        """
        return [''.join(step.get_link_info()) for step in self.step_list]

    @property
    def message(self) -> str:
        """
        Get the message for this plan
        :return: the message
        """
        if self._message:
            return self._message
        else:
            return 'Total travel time is {} minutes'.format(self.total_time_in_min)

    @message.setter
    def message(self, val) -> None:
        """
        Set the message

        :param val: the message
        """
        self._message = val
