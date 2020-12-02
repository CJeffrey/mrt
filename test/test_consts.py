import os

from mrt.utils.consts import RESOURCES_PATH
from mrt.utils.consts import DEFAULT_STATION_MAP_CSV


class TestConsts:
    def test_consts(self):
        assert os.path.isdir(RESOURCES_PATH)
        assert os.path.isfile(DEFAULT_STATION_MAP_CSV)

