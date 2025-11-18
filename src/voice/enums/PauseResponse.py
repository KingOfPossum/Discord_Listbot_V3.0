from enum import Enum

class PauseResponse(Enum):
    """
    Enum representing the response from the pause command.
    Values:
     PAUSED : The song was successfully paused.
     ALREADY_PAUSED : The song was already paused and can therefore not be paused again.
     NO_SONG : There is no song playing right now.
     ERROR : Something went wrong with the pause command.
    """
    PAUSED = 0
    ALREADY_PAUSED = 1
    NO_SONG = 2
    ERROR = 3