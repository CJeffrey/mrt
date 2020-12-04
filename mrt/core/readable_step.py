from collections import namedtuple

# a namedtuple for human read
ReadableStep = namedtuple(
    'ReadableStep',
    ['action', 'station_details', 'time_details',
     'src_station', 'des_station',
     'src_time', 'des_time']
)
