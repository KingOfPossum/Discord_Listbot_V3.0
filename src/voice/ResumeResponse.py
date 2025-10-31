from enum import Enum

class ResumeResponse(Enum):
    RESUMED = 1
    ALREADY_PLAYING = 2
    NO_SONG = 3
    ERROR = 4