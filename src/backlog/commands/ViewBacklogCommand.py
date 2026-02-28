from backlog.BacklogList import BacklogList
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

class ViewBacklogCommand(Command):
    """
    Command for viewing the backlog.
    """

    @commands.command(name="viewBacklog",aliases=["ViewBacklog","VIEWBACKLOG","view_backlog","View_Backlog","VIEW_BACKLOG","backlog","Backlog","BACKLOG"])
    async def execute(self, ctx):
        """
        Handles the viewBacklog command to display the user's backlog.
        Adds buttons to view other user`s backlogs as well.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel, "You are Not Allowed to use this command")
            return

        backlog_list = BacklogList(ctx.author)
        await backlog_list.send_list(ctx.channel)

    def help(self) -> str:
        """
        Provides help information for the command.
        :return: The help string for the command.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}viewBacklog` - View your backlog\n"