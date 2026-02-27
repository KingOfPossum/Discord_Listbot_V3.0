import discord

from common.ConfigLoader import ConfigLoader
from common.GameEntry import GameEntry
from common.MessageManager import MessageManager
from database.DatabaseCollection import DatabaseCollection

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

        config = ConfigLoader.get_config()

        split_msg = message.content.split()
        if split_msg[0].startswith(config.command_prefix):
            return " ".join(split_msg[1:])

        return ""

    @staticmethod
    async def game_exists(game_name: str,user_id: int = None,ctx: discord.Interaction = None,interaction: discord.Interaction = None) -> tuple[str,GameEntry]:
        """
        Checks if a game exists in the database.
        :param ctx: The context in which the command was invoked
        :param interaction: The interaction object if the command was invoked through an interaction.
        :param game_name: The name of the game to check.
        :param user_id: The ID of the user who owns the game entry, if applicable.
        :return: Tuple containing the game name and the GameEntry object if it exists, otherwise None.
        """
        if ctx:
            if user_id is None:
                user_id = ctx.author.id
            game_entry = DatabaseCollection.list_database.get_game_entry(game_name, user_id)
        elif interaction:
            if user_id is None:
                user_id = interaction.user.id
            game_entry = DatabaseCollection.list_database.get_game_entry(game_name, user_id)
        else:
            raise ValueError("Either ctx or interaction must be provided")

        if game_entry is None:
            channel = ctx.channel if ctx else interaction.channel
            await MessageManager.send_error_message(channel, f"Game \"{game_name}\" not found, please provide a Valid Game Name")
            return None
        else:
            print(f"\nFound GameEntry:\n {game_entry}\n")
            return game_name, game_entry
