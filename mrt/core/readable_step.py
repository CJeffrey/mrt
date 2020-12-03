from collections import namedtuple

ReadableStep = namedtuple(
    'ReadableStep',
    ['action', 'station_details', 'time_details']
)
