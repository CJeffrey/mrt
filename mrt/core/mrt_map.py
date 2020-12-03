import csv
from datetime import datetime
from collections import defaultdict
import logging

from ..utils.mrt_logger import do_logging
from ..utils.singleton import Singleton
from .mrt_station import MRTStation
from .exceptions import WrongCSVFormatError, InvalidStationKeyError
from ..utils.consts import OPEN_DATE_FORMAT, OPEN_DATE_FORMAT_M_Y
from ..utils.consts import DEFAULT_STATION_MAP_CSV

logger = logging.getLogger(__name__)


class MRTMap(metaclass=Singleton):
    """
    This is a Singleton Class.
    A Map of the MRT
    """

    def __init__(self):
        """
        init the name2station, key2station
        """
        # store the mapping from name to node
        self._name2station = defaultdict(list)
        # store the mapping from key to node
        self._key2station = {}
        self.init()

    def init(self, csv_file=None) -> None:
        """
        Init from the csv file

        :param csv_file: if None, the default csv file will be used
        """
        csv_file = DEFAULT_STATION_MAP_CSV if csv_file is None else csv_file
        self.build_from_csv_file(csv_file)

    def clean(self):
        """
        Clean all data in this object
        """
        self._name2station.clear()
        self._key2station.clear()

    @property
    def name2station(self) -> dict:
        return self._name2station

    @property
    def key2station(self) -> dict:
        return self._key2station

    @do_logging
    def build_from_csv_file(self, csv_file) -> None:
        """
        Build this map from a pre designed csv file.
        The csv file should have below structure (head included):

            Station Code,Station Name,Opening Date
            NS1,Jurong East,10 March 1990
            ...

        :param csv_file: the csv data file
        """
        logger.info('clean and build_from_csv_file')
        self.clean()

        with open(csv_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            # skip the first head line
            next(csv_reader)

            last_station = None
            for line in csv_reader:
                station = self.get_station_from_line(line)
                if station.key in self.key2station:
                    raise InvalidStationKeyError('key: {} is duplicated'.format(station.key))

                self.connect_stations(last_station, station)
                last_station = station

                for same_name_station in self.name2station[station.name]:
                    self.connect_stations(same_name_station, station)

                self.key2station[station.key] = station
                self.name2station[station.name].append(station)

    def get_station_from_line(self, line: list) -> MRTStation:
        """
        Build MRTStation object from a list of data.

        :param line: should contains key, name, open_date info
                     e.g. "NS7,Kranji,10 February 1996"
        :return: the MRTStation object
        """
        if len(line) != 3:
            raise WrongCSVFormatError(line)
        open_date = self.get_date_time_from_str(line[2])
        return MRTStation(line[0], line[1], open_date)

    @staticmethod
    def get_date_time_from_str(time_str: str) -> datetime:
        """
        Get datetime object from a string.
        Will try several formats. A WrongCSVFormatError will be raised if no format meets

        :param time_str: str which contains the datetime info
        :return: the datetime object
        """
        date_formats = [OPEN_DATE_FORMAT, OPEN_DATE_FORMAT_M_Y]
        open_date = None

        # will try the possible format in the format list
        for date_format in date_formats:
            try:
                open_date = datetime.strptime(time_str, date_format)
            except ValueError:
                pass
            if open_date is not None:
                break

        if open_date is None:
            raise WrongCSVFormatError('can not parse {}'.format(time_str))

        return open_date

    @staticmethod
    def connect_stations(s1: MRTStation, s2: MRTStation) -> None:
        """
        Connect two stations

        :param s1: The connecting station object
        :param s2: The connecting station object
        """
        if s1 is None or s2 is None:
            return

        if s1.line_tag == s2.line_tag or s1.name == s2.name:
            s1.add_next_station(s2)
            s2.add_next_station(s1)

    def get_station_by_key(self, key: str) -> MRTStation:
        """
        Get the station by station key.
        Only return a single MRTStation object

        :param key: the station key
        :return: the returned MRTStation object
        """
        return self.key2station[key]

    def get_station_by_name(self, name: str) -> list:
        """
        Get the station by station name
        Will return a list of MRTStation object

        :param name: the station name
        :return: the returned list
        """
        return self.name2station[name]
