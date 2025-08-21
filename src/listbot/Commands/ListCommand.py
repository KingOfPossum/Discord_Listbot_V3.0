from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

from database.Database import Database
from listbot.Commands.GameList import GameList

class ListCommand(Command):
    """
    Command that will list all games of a specific user from the database.
    """
    def __init__(self,database: Database):
        self.database = database

    @commands.command(name="list")
    async def execute(self,ctx):
        """
        Handles the 'list' command to list all games of a specific user.
        This command will check if the user is accepted and if they are, it will
        retrieve and display the list of games for that user.
        :param ctx: the context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        game_list = GameList(self.database,ctx)
        await game_list.send_list()

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}list` - List all games from the list.\n"