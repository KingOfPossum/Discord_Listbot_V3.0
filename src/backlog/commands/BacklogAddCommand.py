from common.BacklogEntry import BacklogEntry
from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.BacklogDatabase import BacklogDatabase
from discord.ext import commands

class BacklogAddCommand(Command):
    """
    Command for adding games into the backlog.
    """
    def __init__(self,backlog_database:BacklogDatabase):
        self.backlog_database = backlog_database

    @commands.command(name="backlogAdd", aliases=["BacklogAdd","backlogadd","backlog_add","Backlog_Add","BACKLOGADD","BACKLOG_ADD","addBacklog","AddBacklog","ADDBACKLOG","add_backlog","Add_Backlog","ADD_BACKLOG"])
    async def execute(self, ctx):
        """
        Adds the provided game into the backlog of the command invoker.
        If the game is already in the backlog, nothing will be changed.
        :param ctx: The context of the command.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel, "You are Not Allowed to use this command")
            return

        game_name = BotUtils.get_message_content(ctx.message)

        if not game_name or game_name == "":
            await MessageManager.send_error_message(ctx.channel,"No game name provided")
            return

        if self.backlog_database.get_entry(game_name,ctx.author.name):
            await MessageManager.send_message(ctx.channel,f"Game {game_name} is already in backlog")
            return

        self.backlog_database.add_entry(BacklogEntry(game_name,ctx.author.name,None))
        await MessageManager.send_message(ctx.channel,f"Added {game_name} to backlog")

    def help(self) -> str:
        """
        Provides help information for the command.
        :return: The help string for the command.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}backlogAdd` `gameName` - Adds the game to your backlog\n"