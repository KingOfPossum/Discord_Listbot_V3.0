import discord

from common.BacklogEntry import BacklogEntry
from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.BacklogDatabase import BacklogDatabase
from discord.ext import commands

class BacklogRemoveCommand(Command):
    """
    Command for removing games from the backlog
    """
    def __init__(self,backlog_database: BacklogDatabase):
        self.backlog_database = backlog_database

    @commands.command(name="backlogRemove",aliases=["BacklogRemove","backlog_remove","BACKLOG_REMOVE","Backlog_Remove","backlogremove","removeBacklog","RemoveBacklog","REMOVEBACKLOG","remove_backlog","Remove_Backlog","REMOVE_BACKLOG"])
    async def execute(self, ctx):
        """
        Removes the provided game from the backlog of the command invoker.
        :param ctx: The context of the command.
        :return:
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        game_name = BotUtils.get_message_content(ctx.message)
        entry = BacklogEntry(game_name,ctx.author.id,None)
        await BacklogRemoveCommand.remove_backlog_entry(entry,self.backlog_database,ctx.channel)

    def help(self) -> str:
        return f"- `{ConfigLoader.get_config().command_prefix}backlogRemove` `gameName` - Removes a game from your backlog\n"

    @staticmethod
    async def remove_backlog_entry(entry: BacklogEntry,backlog_database:BacklogDatabase,channel:discord.TextChannel):
        backlog_database.remove_entry(entry)
        await MessageManager.send_message(channel,f"Removed {entry.game_name} from backlog")