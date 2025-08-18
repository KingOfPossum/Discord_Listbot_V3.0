from discord.ext import commands

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from database.Database import Database


class RemoveCommand(Command):
    """
    Command that will remove a game from the list.
    """

    def __init__(self, database: Database):
        self.database = database

    @commands.command(name="remove")
    async def execute(self, ctx):
        """
        Handles the 'remove' command to remove a game from the list.
        This command will check if the game exists in the database and if it does, it will
        remove the game entry from the database.
        :param ctx: the context in which the command was invoked
        """
        game_name = BotUtils.get_message_content(ctx.message)
        game = await BotUtils.game_exists(game_name,self.database,ctx=ctx)
        if not game:
            return

        game_name, game_entry = game
        self.database.remove_entry(game_entry)
        await ctx.send(f"**Removed {game_name}**")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}remove` `gameName` - Removes a game from the list.\n"