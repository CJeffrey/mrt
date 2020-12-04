from mrt.core.mrt_map import MRTMap
from mrt.utils.consts import DEFAULT_STATION_MAP_CSV
from . import get_data_file_path


class TestMRTMap:
    def test_build_from_file_default(self):
        """
        Test the default loader working on default csv file
        """
        mrt_map = MRTMap()
        assert len(mrt_map.key2station) != 0
        assert len(mrt_map.name2station) != 0

    def test_build_csv_1(self):
        """
        Test build from customized csv file, and check the inner values
        NS1<->NS2<->NS6
               |
              TE1
        """
        scv_file_name = get_data_file_path('map1.csv')
        mrt_map = MRTMap()
        mrt_map.build_from_csv_file(scv_file_name)

        assert len(mrt_map.key2station) == 4
        assert len(mrt_map.name2station) == 3

        ns1 = mrt_map.key2station['NS1']
        ns2 = mrt_map.key2station['NS2']
        ns6 = mrt_map.key2station['NS6']
        te1 = mrt_map.key2station['TE1']

        assert len(ns1.next_stations) == 1
        assert len(ns2.next_stations) == 3
        assert len(ns6.next_stations) == 1
        assert len(te1.next_stations) == 1
