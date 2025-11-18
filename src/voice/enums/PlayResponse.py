from enum import Enum

class PlayResponse(Enum):
    SUCCESS = 0
    ANOTHER_SONG_IS_PLAYING = 1
    ERROR = 2