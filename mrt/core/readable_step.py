from collections import namedtuple

# a namedtuple for human read
ReadableStep = namedtuple(
    'ReadableStep',
    ['action', 'station_details', 'time_details']
)
