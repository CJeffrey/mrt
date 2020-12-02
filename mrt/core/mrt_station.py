from collections.abc import Hashable
from datetime import datetime
from copy import copy


class MRTStation(Hashable):
    def __init__(self, key: str, name: str, open_date: datetime) -> None:
        """

        :param key: the key of the station
        :param name: the name of the station
        :param open_date: the open date of the station
        """
        self._key = key
        self._name = name
        self._open_date = open_date
        self._line_tag = self._init_line_tag()
        self._next_stations = set()

    def __hash__(self) -> int:
        return hash(self._key)

    def __eq__(self, other):
        if not isinstance(other, MRTStation):
            return False
        return self._key == other._key

    def _init_line_tag(self) -> str:
        """
        init line_tag from _key

        :return:
        """
        return self._key[:2]

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> str:
        return self._name

    @property
    def open_date(self) -> datetime:
        return self._open_date

    @property
    def line_tag(self) -> str:
        return self._line_tag

    @property
    def next_stations(self) -> set:
        return copy(self._next_stations)

    def add_next_station(self, station) -> None:
        self._next_stations.add(station)
