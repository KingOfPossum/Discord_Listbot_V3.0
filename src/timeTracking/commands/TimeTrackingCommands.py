from database_.DatabaseCollection import DatabaseCollection
from discord.ext import commands
from timeTracking.commands.TimeStatsCommand import TimeStatsCommand

class TimeTrackingCommands:
    """
    Collection of commands related to time tracking.
    This class registers these commands to the provided bot instance.
    """
    def __init__(self,databases: DatabaseCollection):
        """
        Initializes the TimeTrackingCommands.
        """
        self.databases = databases

    async def register(self,bot:commands.Bot):
        """
        Registers the time tracking commands for the bot.
        :param bot: The Discord bot instance to register commands with.
        """
        await bot.add_cog(TimeStatsCommand(self.databases.time_database))
        print("Registered TimeTrackingCommands cogs.")
