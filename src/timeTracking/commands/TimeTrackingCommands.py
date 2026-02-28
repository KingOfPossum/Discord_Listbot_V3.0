from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands
from timeTracking.commands.TimeStatsCommand import TimeStatsCommand

class TimeTrackingCommands:
    """
    Collection of commands related to time tracking.
    This class registers these commands to the provided bot instance.
    """

    async def register(self,bot:commands.Bot):
        """
        Registers the time tracking commands for the bot.
        :param bot: The Discord bot instance to register commands with.
        """
        await bot.add_cog(TimeStatsCommand())
        print("Registered TimeTrackingCommands cogs.")
