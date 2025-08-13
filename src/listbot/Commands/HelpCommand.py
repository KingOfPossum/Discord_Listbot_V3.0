from common.Command import Command
from discord.ext import commands
from listbot.Commands.AddCommand import AddCommand
from listbot.Commands.CompletedCommand import CompletedCommand
from listbot.Commands.RemoveCommand import RemoveCommand
from listbot.Commands.ReplayedCommand import ReplayedCommand
from listbot.Commands.UpdateCommand import UpdateCommand
from listbot.Commands.ViewCommand import ViewCommand


class HelpCommand(Command):
    """
    Command that will display the help message for all commands.
    """

    def __init__(self):
        self.list_commands = [AddCommand(database=None),UpdateCommand(database=None),RemoveCommand(database=None),ReplayedCommand(database=None),CompletedCommand(database=None),ViewCommand(database=None)]

    @commands.command(name="help")
    async def execute(self, ctx):
        """
        Handles the 'help' command to display the help message.
        This command will send a message with the available commands and their descriptions.
        :param ctx: the context in which the command was invoked
        """
        await ctx.send(self.help())

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return "**List Commands:**\n" + "".join([command.help() for command in self.list_commands])