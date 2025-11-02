from enum import Enum

class PlayStatus(Enum):
    """
    Enum representing the playing status of the bot.
    Values:
    NOTHING : There is no song playing right now.
    PLAYING : The bot is playing a song right now.
    PAUSED : The current song is paused right now.
    """
    NOTHING = 0
    PLAYING = 1
    PAUSED = 2