import discord

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.ListDatabase import ListDatabase
from discord.ext import commands

class ReplayedCommand(Command):
    """
    Command that will change the replay status of a game in the list.
    """
    def __init__(self, database: ListDatabase):
        self.database = database

    @staticmethod
    async def change_replayed_status(game_name: str, database: ListDatabase, ctx: discord.Interaction = None, interaction: discord.Interaction = None):
        """
        Changes the replay status of a game.
        This function will check if the game exists in the database and if it does, it will
        toggle the replayed status of the game.
        :param game_name: The name of the game to change the replay status for
        :param database: The database instance to use
        :param ctx: The context in which the command was invoked (optional)
        :param interaction: The interaction that triggered the command (optional)
        :return: The new game entry with updated replay status
        """
        game = await BotUtils.game_exists(game_name,database,ctx=ctx,interaction=interaction)
        if game is None:
            return

        game_name, old_game_entry = game
        new_game_entry = old_game_entry

        new_game_entry.replayed = not old_game_entry.replayed
        print(f"Replayed status changed to: {new_game_entry.replayed}\n")

        database.put_game(new_game_entry)

        return new_game_entry

    @commands.command(name="replayed",aliases=["Replayed","rp","replayedGame","ReplayedGame","REPLAYED","REPLAYEDGAME","replayed_game","Replayed_Game","REPLAYED_GAME","Replayedgame","replayedgame"])
    async def execute(self,ctx):
        """
        Handles the 'replayed' command to change the replay status of a game.
        This command will check if the game exists in the database and if it does, it will
        toggle the replayed status of the game.
        :param ctx: the context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        game_name = BotUtils.get_message_content(ctx.message)
        new_game_entry = await self.change_replayed_status(game_name=game_name,database=self.database,ctx=ctx)

        emojis = [Emojis.CROSS_MARK, Emojis.CHECK_MARK]
        await ctx.send(f"**Changed replay status of {game_name} to: {emojis[new_game_entry.replayed]}**")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}replayed` `gameName` - Mark a game as replayed.\n"