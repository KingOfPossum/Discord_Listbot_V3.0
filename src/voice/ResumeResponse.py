from enum import Enum

class ResumeResponse(Enum):
    """
    Enum representing the possible resume responses.
    Values:
    RESUMED : Song resumed successfully.
    ALREADY_PLAYING : The song is already playing/not paused.
    NO_SONG : There is no song playing right now to resume.
    ERROR : Something went wrong with resume command.
    """
    RESUMED = 1
    ALREADY_PLAYING = 2
    NO_SONG = 3
    ERROR = 4