from backlog.commands.BacklogAddCommand import BacklogAddCommand
from backlog.commands.BacklogRemoveCommand import BacklogRemoveCommand
from backlog.commands.GetRecommendationCommand import GetRecommendationCommand
from backlog.commands.RecommendCommand import RecommendCommand
from backlog.commands.ViewBacklogCommand import ViewBacklogCommand
from common.Command import Command
from discord.ext import commands
from general.commands.RandomizeCommand import RandomizeCommand
from general.commands.RandomizeNumCommand import RandomizeNumCommand
from general.commands.ActivateBotRepliesCommand import ActivateBotRepliesCommand
from general.commands.DeactivateBotRepliesCommand import DeactivateBotRepliesCommand
from general.commands.ToggleBotRepliesCommand import ToggleBotRepliesCommand
from listbot.commands.AddCommand import AddCommand
from listbot.commands.CompletedCommand import CompletedCommand
from listbot.commands.ConsolesCommand import ConsolesCommand
from listbot.commands.InfoCommand import InfoCommand
from listbot.commands.ListCommand import ListCommand
from listbot.commands.RemoveCommand import RemoveCommand
from listbot.commands.ReplayedCommand import ReplayedCommand
from listbot.commands.StatsCommand import StatsCommand
from listbot.commands.UpdateCommand import UpdateCommand
from listbot.commands.ViewCommand import ViewCommand
from timeTracking.commands.TimeStatsCommand import TimeStatsCommand
from tokenSystem.commands.AddTokenCommand import AddTokenCommand
from tokenSystem.commands.RemoveCoinCommand import RemoveCoinCommand
from tokenSystem.commands.SetNeededCoinsCommand import SetNeededCoinsCommand
from tokenSystem.commands.ViewTokensCommand import ViewTokensCommand
from voice.commands.JoinCommand import JoinCommand
from voice.commands.LeaveCommand import LeaveCommand

class HelpCommand(Command):
    """
    Command that will display the help message for all commands.
    """
    def __init__(self):
        self.general_commands = [RandomizeNumCommand(),RandomizeCommand(),ActivateBotRepliesCommand(),DeactivateBotRepliesCommand(),ToggleBotRepliesCommand()]
        self.list_commands = [AddCommand(list_database=None,token_database=None,backlog_database=None),UpdateCommand(database=None),RemoveCommand(database=None),ReplayedCommand(database=None),CompletedCommand(database=None),ViewCommand(database=None),ListCommand(database=None),
                              ConsolesCommand(),StatsCommand(list_database=None),InfoCommand()]
        self.token_commands = [AddTokenCommand(database=None),RemoveCoinCommand(database=None),SetNeededCoinsCommand(database=None),ViewTokensCommand(database=None)]
        self.time_commands = [TimeStatsCommand(time_database=None)]
        self.voice_commands = [JoinCommand(),LeaveCommand()]
        self.backlog_commands = [BacklogAddCommand(None),BacklogRemoveCommand(None),RecommendCommand(None),GetRecommendationCommand(None),ViewBacklogCommand(None)]

    @commands.command(name="help",aliases=["Help","HELP","h","commands","Commands","COMMANDS"])
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
        general_commands_help = "**General Commands:**\n" + "".join([command.help() for command in self.general_commands])
        list_commands_help = "**List Commands:**\n" + "".join([command.help() for command in self.list_commands])
        tokens_command_help = "**Token Commands:**\n" + "".join(command.help() for command in self.token_commands)
        time_command_help = "**Time Tracking Commands:**\n" + "".join(command.help() for command in self.time_commands)
        voice_command_help = "**Voice Commands:**\n" + "".join(command.help() for command in self.voice_commands)
        backlog_command_help = "**Backlog Commands:**\n" + "".join(command.help() for command in self.backlog_commands)
        return general_commands_help + "\n" + list_commands_help + "\n" + tokens_command_help + "\n" + time_command_help + "\n" + backlog_command_help + "\n" + voice_command_help
