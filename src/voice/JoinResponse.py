from enum import Enum

class JoinResponse(Enum):
    """
    Enum representing the possible join responses.
    Values:
     JOINED : Successfully joined the voice channel.
     MOVED : Successfully moved to the voice channel.
     ALREADY_IN_CHANNEL : Bot was already in the correct voice channel.
     USER_NOT_IN_VOICE : The user who invoked the join command was in no voice channel.
     FAILED : Something went wrong with the join command.
    """
    JOINED = 1
    MOVED = 2
    ALREADY_IN_CHANNEL = 3
    USER_NOT_IN_VOICE = 4
    FAILED = 5

