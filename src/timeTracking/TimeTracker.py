from discord.ext import commands,tasks

class TimeTracker(commands.Cog):
    """Time Tracker Cog. This cog tracks the time spent on various activities."""

    def __init__(self,bot: commands.Bot):
        """
        Initializes the TimeTracker cog with a bot instance.
        :param bot: The bot instance to which this cog will be added.
        """
        self.bot = bot

    async def cog_load(self):
        """Is executed when the TimeTracker cog is loaded"""
        self.track_time.start()
        print("Time tracker loaded")

    async def cog_unload(self):
        """Is executed when the TimeTracker cog is unloaded"""
        self.track_time.cancel()
        print("Time tracker unloaded")

    @tasks.loop(seconds = 10)
    async def track_time(self):
        """
        The tracking task that runs every 10 seconds.
        This will track the time spent on any activity.
        """
        print("Tracking time...")

    @track_time.before_loop
    async def before_track_time(self):
        """This will ensure that the TimeTracker only starts after the bot is ready."""
        await self.bot.wait_until_ready()