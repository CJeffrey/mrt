from collections.abc import Hashable
from datetime import datetime
from copy import copy

from .mrt_line_tag import LineTags
from .exceptions import InvalidLineTagError
from .exceptions import InvalidTransportError


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
        """
        Use the hash of key instead

        :return: hash value
        """
        return hash(self._key)

    def __eq__(self, other):
        """
        Compared by the key

        :param other: the other MRTStation object
        :return: equal or not
        """
        if not isinstance(other, MRTStation):
            return False
        return self.key == other.key

    def __lt__(self, other):
        """
        Compare by the key

        :param other: the other MRTStation object
        :return: less than or not
        """
        if not isinstance(other, MRTStation):
            raise TypeError('Must compare with a MRTStation object')
        return self.key < other.key

    def _init_line_tag(self) -> LineTags:
        """
        init line_tag from _key
        InvalidLineTagError will be raised if the _key is invalid

        :return: LineTags object
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
        """
        Add new station into the next station

        :param station: the connecting station
        """
        self._next_stations.add(station)

    def __repr__(self):
        return 'key: {key}, name: {name}, open_date: {open_date}, line_tag: {line_tag}'.format(
            key=self.key, name=self.name, open_date=self.open_date, line_tag=self.line_tag
        )

    def get_travel_type(self, other) -> LineTags:
        """
        Get the travel type with the other station
        Return the line tag if they are in the same line
        Return LINE_CHANGE if station name is the same
        InvalidTransportError would be raised if this travel type is not supported

        :param other: the other MRTStation
        :return: the travel type
        """
        if not isinstance(other, MRTStation):
            raise TypeError('Must compare with a MRTStation object')

        if self.key == other.key:
            raise InvalidTransportError('can not transfer in the same station {} to {}'.format(self, other))
        if other not in self.next_stations:
            raise InvalidTransportError('can not transfer in unconnected stations {} to {}'.format(self, other))

        if self.line_tag == other.line_tag:
            line_tag = self.line_tag
        elif self.name == other.name:
            line_tag = LineTags.LINE_CHANGE
        else:
            raise InvalidTransportError('can not transfer from {} to {}'.format(self, other))

        return line_tag

    def get_name_with_key(self) -> str:
        """
        Get the name with key info
        Format {<name>}(<key>)

        :return: name with key info
        """
        return '{name}({key})'.format(name=self.name, key=self.key)

    def get_link_info(self) -> list:
        """
        Get all the link info about this node
        Format [{'source': <source>, 'target':<target>, 'type':<LineTags>}, ... ]

        :return: link info
        """
        link_info_list = []
        for next_station in self.next_stations:
            link_info_list.append(
                self.get_link_info_with_station(next_station)
            )
        return link_info_list

    def get_link_info_with_station(self, other):
        return sorted([self.get_name_with_key(), other.get_name_with_key()]) + [self.get_travel_type(other).name]
