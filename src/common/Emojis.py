from common.ConfigLoader import ConfigLoader

class Emojis:
    """
    A class to hold emoji constants.
    """
    CHECK_MARK = "✅"
    CROSS_MARK = "❌"
    CONSOLES = ConfigLoader.get_config().consoles
    REVIEW = "📜"
    RANKINGS = ["🥇", "🥈", "🥉"]
    first_place = "🥇"
    second_place = "🥈"
    third_place = "🥉"

    @staticmethod
    def get_console_emoji(console_name:str):
        """
        Returns the emoji for the specified console.
        If the console does not exist, it returns the console name itself.
        :param console_name: The name of the console.
        :return: The emoji for the console or the console name if not found.
        """
        if console_name in Emojis.CONSOLES:
            return Emojis.CONSOLES[console_name]
        return console_name