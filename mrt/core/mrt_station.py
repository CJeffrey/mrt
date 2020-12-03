from collections.abc import Hashable
from datetime import datetime
from copy import copy

from .mrt_line_tag import LineTags
from .exceptions import InvalidLineTagError


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

    def _init_line_tag(self) -> LineTags:
        """
        init line_tag from _key

        :return:
        """
        tag_str = self._key[:2]
        try:
            return LineTags[tag_str]
        except KeyError:
            raise InvalidLineTagError('invalid line tag: {}'.format(tag_str))

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
    def line_tag(self) -> LineTags:
        return self._line_tag

    @property
    def next_stations(self) -> set:
        return copy(self._next_stations)

    def add_next_station(self, station) -> None:
        self._next_stations.add(station)

    def __repr__(self):
        return 'key: {key}, name: {name}, open_date: {open_date}, line_tag: {line_tag}'.format(
            key=self.key, name=self.name, open_date=self.open_date, line_tag=self.line_tag
        )
