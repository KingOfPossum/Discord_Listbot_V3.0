from enum import Enum

class StopResponse(Enum):
    """
    Enum for results of the stop command.
    Values:
    STOPPED_SONG : Song stopped successfully.
    NO_SONG : There is no song to stop.
    ERROR : Something went wrong with stop command.
    """
    STOPPED_SONG= 0
    NO_SONG = 1
    ERROR = 2