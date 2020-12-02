import csv
from datetime import datetime
from collections import defaultdict

from ..utils.mrt_logger import do_logging
from .mrt_station import MRTStation
from .exceptions import WrongCSVFormatError, InvalidStationKeyError
from ..utils.consts import OPEN_DATE_FORMAT, OPEN_DATE_FORMAT_M_Y


class MRTMap:
    def __init__(self):
        # store the mapping from name to node
        self._name2station = defaultdict(list)
        # store the mapping from key to node
        self._key2station = {}

    @property
    def name2station(self) -> dict:
        return self._name2station

    @property
    def key2station(self) -> dict:
        return self._key2station

    @do_logging
    def build_from_csv_file(self, csv_file):
        with open(csv_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
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

        :param line: should contains key, name, open_date info
                     e.g. "NS7,Kranji,10 February 1996"
        :return:
        """
        if len(line) != 3:
            raise WrongCSVFormatError(line)
        open_date = self.get_date_time_from_str(line[2])
        return MRTStation(line[0], line[1], open_date)

    def get_date_time_from_str(self, time_str: str) -> datetime:
        date_formats = [OPEN_DATE_FORMAT, OPEN_DATE_FORMAT_M_Y]
        open_date = None

        for date_format in date_formats:
            try:
                open_date = datetime.strptime(time_str, date_format)
            except ValueError as e:
                pass
            if open_date is not None:
                break

        if open_date is None:
            raise WrongCSVFormatError('can not parse {}'.format(time_str))

        return open_date

    def connect_stations(self, s1: MRTStation, s2: MRTStation):
        if s1 is None or s2 is None:
            return

        if s1.line_tag == s2.line_tag or s1.name == s2.name:
            s1.add_next_station(s2)
            s2.add_next_station(s1)

