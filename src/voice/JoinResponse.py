from enum import Enum

class JoinResponse(Enum):
    JOINED = 1
    MOVED = 2
    ALREADY_IN_CHANNEL = 3
    USER_NOT_IN_VOICE = 4
    FAILED = 5

