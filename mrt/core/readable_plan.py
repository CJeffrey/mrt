from .readable_step import ReadableStep


class ReadablePlan:
    def __init__(self):
        self._step_list = []

    @property
    def step_list(self) -> list:
        return self._step_list

    def get_readable_outcome(self):
        out_come = []

        for step in self.step_list:
            single_outcome = ReadableStep(
                action=step.get_readable_action(),
                station_details=step.get_readable_station_details(),
                time_details=step.get_readable_time_details(),
            )
            out_come.append(single_outcome)

        return out_come
