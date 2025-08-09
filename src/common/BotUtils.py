import discord

from common.ConfigLoader import ConfigLoader


class BotUtils:
    @staticmethod
    def get_message_content(message: discord.Message) -> str:
        """
        Returns the content of a message, handling both text and attachments.
        :param message: The Discord message object.
        :return: The content of the message as a string.
        """
        if message.content is None:
            return ""

        config = ConfigLoader.load()

        split_msg = message.content.split()
        if split_msg[0].startswith(config.command_prefix):
            return " ".join(split_msg[1:])

        return ""
