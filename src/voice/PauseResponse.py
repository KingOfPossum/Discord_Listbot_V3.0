from enum import Enum

class PauseResponse(Enum):
    PAUSED = 0
    ALREADY_PAUSED = 1
    NO_SONG = 2
    ERROR = 3