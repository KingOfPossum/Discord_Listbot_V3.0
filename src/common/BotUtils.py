import discord

from common.ConfigLoader import ConfigLoader
from common.GameEntry import GameEntry
from database.Database import Database

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
    async def game_exists(ctx: discord.Interaction,database: Database) -> tuple[str,GameEntry]:
        """
        Checks if a game exists in the database.
        :param ctx: The context in which the command was invoked
        :param database: The database instance to check for the game entry.
        :return: Tuple containing the game name and the GameEntry object if it exists, otherwise None.
        """
        game_name = BotUtils.get_message_content(ctx.message)
        game_entry = database.get_game_entry(game_name, ctx.author.name)

        if game_entry is None:
            await ctx.send(f"**{game_name} not found!**")
            return None
        else:
            print(f"\nFound GameEntry:\n {game_entry}\n")
            return game_name, game_entry
