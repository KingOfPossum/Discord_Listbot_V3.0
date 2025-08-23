import discord

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.ListDatabase import ListDatabase
from discord.ext import commands

class CompletedCommand(Command):
    def __init__(self,database: ListDatabase):
        self.database = database

    @staticmethod
    async def change_completed_status(game_name: str,database: ListDatabase,ctx: discord.Interaction = None,interaction: discord.Interaction = None):
        """
        Changes the completion status of a game in the database.
        This function will check if the game exists in the database and if it does, it will
        toggle the completion status of the game.
        If the game does not exist, it will send an error message.
        :param game_name: Name of the game to change the completion status for.
        :param database: The database instance to interact with.
        :param ctx: The context in which the command was invoked, if applicable.
        :param interaction: The interaction object, if applicable.
        :return: GameEntry object with updated completion status or None if the game does not exist.
        """
        game = await BotUtils.game_exists(game_name, database,ctx=ctx,interaction=interaction)
        if game is None:
            return

        game_name, old_game_entry = game
        new_game_entry = old_game_entry

        new_game_entry.hundred_percent = not old_game_entry.hundred_percent
        print(f"Completion status changed to: {new_game_entry.hundred_percent}\n")

        database.put_game(new_game_entry, old_game_entry)

        return new_game_entry

    @commands.command(name="completed")
    async def execute(self, ctx):
        """
        Handles the 'completed' command to change the completed status of a game.
        This command will check if the game exists in the database and if it does, it will
        toggle the replayed status of the game.
        :param ctx: the context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        game_name = BotUtils.get_message_content(ctx.message)
        new_game_entry = await self.change_completed_status(game_name=game_name,database=self.database,ctx=ctx)

        emojis = [Emojis.CROSS_MARK, Emojis.CHECK_MARK]
        await ctx.send(f"**Changed completion status of {game_name} to: {emojis[new_game_entry.hundred_percent]}**")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}completed` `gameName` - Changes the completion status of a game\n"