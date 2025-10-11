from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

class ConsolesCommand(Command):
    """Command that will display the list of supported consoles."""

    @commands.command(name="consoles")
    async def execute(self, ctx):
        """
        Handles the 'consoles' command to display the list of supported consoles.
        This command will send a message with the names of all supported consoles.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        consoles_txt = "\n".join([f"- {console} : {Emojis.CONSOLES[console]}" for console in ConfigLoader.get_config().consoles.keys()])
        await ctx.send(consoles_txt)

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: A string containing the command usage and description.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}consoles` - View the list of supported consoles.\n"