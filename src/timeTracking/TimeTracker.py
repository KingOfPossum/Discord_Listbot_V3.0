from discord.ext import commands,tasks

from common.UserManager import UserManager


class TimeTracker(commands.Cog):
    """Time Tracker Cog. This cog tracks the time spent on various activities."""

    def __init__(self,bot: commands.Bot):
        """
        Initializes the TimeTracker cog with a bot instance.
        :param bot: The bot instance to which this cog will be added.
        """
        self.bot = bot
        self.tracking_dict = None

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

        if self.tracking_dict is None:
            self.create_tracking_dict()

        for user in UserManager.accepted_users:
            if user.activity is None:
                print(f"User {user.name} has no activity")
                continue

            print(f"User {user.name} is playing {user.activity.name}")
            if self.tracking_dict[user.name]["current_activity"] == user.activity.name:
                try:
                    self.tracking_dict[user.name]["activities"][user.activity.name] += 10
                except KeyError:
                    self.tracking_dict[user.name]["activities"][user.activity.name] = 10
            self.tracking_dict[user.name]["current_activity"] = user.activity.name

        print(self.tracking_dict)

        ##Save to database here

    @track_time.before_loop
    async def before_track_time(self):
        """This will ensure that the TimeTracker only starts after the bot is ready."""
        await self.bot.wait_until_ready()

    def create_tracking_dict(self):
        self.tracking_dict = {user.name: {"current_activity": None, "activities":{"Activity1":0}} for user in UserManager.accepted_users}