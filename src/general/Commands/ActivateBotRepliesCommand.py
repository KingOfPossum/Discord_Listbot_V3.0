from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

class ActivateBotRepliesCommand(Command):
    """
    Command to activate bot replies.
    """
    @commands.command(name="activateBotReplies", aliases=['activateReplies'])
    async def execute(self,ctx):
        """
        Execute the command to activate bot replies.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel, "You are Not Allowed to use this command")
            return

        ConfigLoader.update("bot_replies", True)
        await MessageManager.send_message(ctx.channel,"Bot replies have been activated successfully!")

    def help(self) -> str:
        """
        Returns a help message for the command.
        :return: A string containing the help message.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}activateBotReplies`: Activates bot replies.\n"