from common.Command import Command
from discord.ext import commands

from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager


class ActivateBotRepliesCommand(Command):
    """
    Command to activate bot replies.
    """
    @commands.command(name="activateBotReplies", aliases=['activateReplies'])
    async def execute(self,ctx):
        """
        Execute the command to activate bot replies.
        """
        ConfigLoader.update("bot_replies", True)
        await MessageManager.send_message(ctx.channel,"Bot replies have been activated successfully!")

    def help(self) -> str:
        """
        Returns a help message for the command.
        :return: A string containing the help message.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}activateBotReplies`: Activates bot replies.\n"