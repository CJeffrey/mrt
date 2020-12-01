import os.path as path


CUR_PATH = path.dirname(path.abspath(__file__))
RESOURCES_PATH = path.join(CUR_PATH, '..', 'resources')
DEFAULT_STATION_MAP_CSV = path.join(RESOURCES_PATH, 'StationMap.csv')
