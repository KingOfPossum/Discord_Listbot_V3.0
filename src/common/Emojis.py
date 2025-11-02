from common.ConfigLoader import ConfigLoader

class Emojis:
    """
    A class to hold emoji constants.
    """
    CHECK_MARK = "✅"
    CROSS_MARK = "❌"
    REVIEW = "📜"
    RANKINGS = ["🥇", "🥈", "🥉"]
    first_place = "🥇"
    second_place = "🥈"
    third_place = "🥉"
    PAUSE = "⏸️"
    RESUME = "▶️"
    STOP = "⏹️"
    SHUFFLE = "🔀"
    LOOP = "🔁"

    @staticmethod
    def consoles() -> dict:
        return ConfigLoader.get_config().consoles

    @staticmethod
    def get_console_emoji(console_name:str):
        """
        Returns the emoji for the specified console.
        If the console does not exist, it returns the console name itself.
        :param console_name: The name of the console.
        :return: The emoji for the console or the console name if not found.
        """
        if console_name in Emojis.consoles():
            return Emojis.consoles()[console_name]
        return console_name