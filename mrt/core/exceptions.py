"""
Contains all the exceptions for this project
"""


class WrongCSVFormatError(ValueError):
    pass


class InvalidStationKeyError(ValueError):
    pass


class InvalidLineTagError(ValueError):
    pass


class InvalidTransportError(ValueError):
    pass
