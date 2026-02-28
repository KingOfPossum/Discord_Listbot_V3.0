from discord.ext import commands
from listbot.commands.AddCommand import AddCommand
from listbot.commands.CompletedCommand import CompletedCommand
from listbot.commands.ConsolesCommand import ConsolesCommand
from listbot.commands.HelpCommand import HelpCommand
from listbot.commands.InfoCommand import InfoCommand
from listbot.commands.ListCommand import ListCommand
from listbot.commands.RemoveCommand import RemoveCommand
from listbot.commands.ReplayedCommand import ReplayedCommand
from listbot.commands.StatsCommand import StatsCommand
from listbot.commands.UpdateCommand import UpdateCommand
from listbot.commands.ViewCommand import ViewCommand

class ListCommands:
    """
    Collection of commands related to managing the game list.
    This class registers these commands to the provided bot instance.
    """

    async def register(self, bot: commands.Bot):
        """
        Registers the commands in this cog with the provided bot.
        :param bot: The Discord bot instance to register commands with.
        """
        await bot.add_cog(AddCommand())
        await bot.add_cog(UpdateCommand())
        await bot.add_cog(RemoveCommand())
        await bot.add_cog(ReplayedCommand())
        await bot.add_cog(CompletedCommand())
        await bot.add_cog(ViewCommand())
        await bot.add_cog(ListCommand())
        await bot.add_cog(StatsCommand())
        await bot.add_cog(ConsolesCommand())
        await bot.add_cog(InfoCommand())
        await bot.add_cog(HelpCommand())
        print("Registered ListCommands cogs.")