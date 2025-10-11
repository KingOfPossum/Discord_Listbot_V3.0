from common.TimeEntry import TimeEntry
from common.UserManager import UserManager
from database.TimeDatabase import TimeDatabase
from discord.ext import commands,tasks

class TimeTracker(commands.Cog):
    """Time Tracker Cog. This cog tracks the time spent on various activities."""

    def __init__(self,bot: commands.Bot,time_database: TimeDatabase):
        """
        Initializes the TimeTracker cog with a bot instance.
        :param bot: The bot instance to which this cog will be added.
        :param time_database: The TimeDatabase instance for storing and loading time tracking data.
        """
        self.bot = bot
        self.time_database = time_database
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
            self.load_tracking_dict()

        for user in UserManager.accepted_users:
            if user.activity is None:
                continue

            if self.tracking_dict[user.name]["current_activity"] == user.activity.name:
                try:
                    self.tracking_dict[user.name]["activities"][user.activity.name] += 10
                except KeyError:
                    self.tracking_dict[user.name]["activities"][user.activity.name] = 10
                new_entry = TimeEntry(user.name,user.activity.name,self.tracking_dict[user.name]["activities"][user.activity.name])
                self.time_database.put_entry(new_entry)
            self.tracking_dict[user.name]["current_activity"] = user.activity.name

    @track_time.before_loop
    async def before_track_time(self):
        """This will ensure that the TimeTracker only starts after the bot is ready."""
        await self.bot.wait_until_ready()

    def load_tracking_dict(self):
        """
        Loads the tracking dictionary from the database.
        The tracking dictionary is a nested dictionary with the following structure:
        {
            "username": {
                "current_activity": "activity_name",
                "activities": {
                    "activity_name": time_spent_in_seconds,
                    ...
                }
            },
            ...
        }
        :return:
        """
        entries = self.time_database.get_all_time_entries()
        users = self.time_database.get_users()

        new_dict = {}
        for user in users:
            new_dict[user] = {"current_activity": None, "activities": {}}

        for entry in entries:
            new_dict[entry.user]["activities"][entry.activity] = entry.time_spent

        self.tracking_dict = new_dict