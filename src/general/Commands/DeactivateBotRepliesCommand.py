from common.Command import Command
from discord.ext import commands

from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager

class DeactivateBotRepliesCommand(Command):
    """
    Command to activate bot replies.
    """
    @commands.command(name="deactivateBotReplies", aliases=['deactivateReplies'])
    async def execute(self,ctx):
        """
        Execute the command to activate bot replies.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel, "You are Not Allowed to use this command")
            return

        ConfigLoader.update("bot_replies", False)
        await MessageManager.send_message(ctx.channel,"Bot replies have been deactivated successfully!")

    def help(self) -> str:
        """
        Returns a help message for the command.
        :return: A string containing the help message.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}deactivateBotReplies`: Deactivates bot replies.\n"