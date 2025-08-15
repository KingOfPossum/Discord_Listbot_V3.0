from common.ConfigLoader import ConfigLoader

class Emojis:
    """
    A class to hold emoji constants.
    """
    CHECK_MARK = "✅"
    CROSS_MARK = "❌"
    CONSOLES = ConfigLoader.get_config().consoles