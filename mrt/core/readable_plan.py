class ReadablePlan:
    def __init__(self):
        self._step_list = []

    @property
    def step_list(self) -> list:
        return self._step_list
