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

    def test_get_nodes_links(self):
        scv_file_name = get_data_file_path('map1.csv')
        mrt_map = MRTMap()
        mrt_map.build_from_csv_file(scv_file_name)

        nodes_links = mrt_map.get_nodes_links()
        assert nodes_links

        assert len(nodes_links) == 2
        nodes = nodes_links['nodes']
        links = nodes_links['links']

        assert len(nodes) == 4
        assert len(links) == 3

        nodes_name_set = set()
        for node in nodes:
            assert len(node) == 1
            nodes_name_set.add(node['id'])
        assert nodes_name_set == {'NAME1(NS1)', 'NAME2(NS2)', 'NAME6(NS6)', 'NAME2(TE1)'}

        links_set = set()
        for link in links:
            assert len(link) == 3
            links_set.add((link['source'], link['target'], link['type']))

        assert links_set == {('NAME1(NS1)', 'NAME2(NS2)', 'NS'),
                             ('NAME2(NS2)', 'NAME6(NS6)', 'NS'),
                             ('NAME2(NS2)', 'NAME2(TE1)', 'LINE_CHANGE')}
