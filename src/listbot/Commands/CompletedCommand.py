from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from discord.ext import commands
from database.Database import Database

class CompletedCommand(Command):
    def __init__(self,database: Database):
        self.__command_prefix = ConfigLoader.get_config().command_prefix
        self.database = database

    @commands.command(name="completed")
    async def execute(self, ctx):
        """
        Handles the 'completed' command to change the completed status of a game.
        This command will check if the game exists in the database and if it does, it will
        toggle the replayed status of the game.
        :param ctx: the context in which the command was invoked
        """
        game = await BotUtils.game_exists(ctx, self.database)
        if game is None:
            return

        game_name, old_game_entry = game
        new_game_entry = old_game_entry

        new_game_entry.hundred_percent = not old_game_entry.hundred_percent
        print(f"Replayed status changed to: {new_game_entry.hundred_percent}\n")

        self.database.put_game(new_game_entry, old_game_entry)

        emojis = [Emojis.CROSS_MARK, Emojis.CHECK_MARK]
        await ctx.send(f"**Changed replay status of {game_name} to: {emojis[new_game_entry.hundred_percent]}**")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"`{self.__command_prefix}completed` `gameName` - Changes the completed status of a game\n"