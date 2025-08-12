from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from database.Database import Database
from discord.ext import commands

class ReplayedCommand(Command):
    """
    Command that will change the replay status of a game in the list.
    """

    def __init__(self, database: Database):
        self.__command_prefix = ConfigLoader.get_config().command_prefix
        self.database = database

    @commands.command(name="replayed")
    async def execute(self,ctx):
        """
        Handles the 'replayed' command to change the replay status of a game.
        This command will check if the game exists in the database and if it does, it will
        toggle the replayed status of the game.
        :param ctx: the context in which the command was invoked
        """
        game = await BotUtils.game_exists(ctx,self.database)
        if game is None:
            return

        game_name, old_game_entry = game
        new_game_entry = old_game_entry

        new_game_entry.replayed = not old_game_entry.replayed
        print(f"Replayed status changed to: {new_game_entry.replayed}\n")

        self.database.put_game(new_game_entry, old_game_entry)

        emojis = [Emojis.CROSS_MARK, Emojis.CHECK_MARK]
        await ctx.send(f"**Changed replay status of {game_name} to: {emojis[new_game_entry.replayed]}**")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"`{self.__command_prefix}replayed` `gameName` - Mark a game as replayed\n"