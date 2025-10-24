import asyncio
import os
import subprocess
import sys

from discord.ext import commands, tasks
from listbot.BotEvents import BotEvents

class Updater(commands.Cog):
    """
    Cog containing update task which automatically looks for updates, installs them and then restarts the bot.
    """
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    async def cog_load(self):
        """Is executed when the Updater cog is loaded"""
        self.update.start()
        print("Updater loaded")

    async def cog_unload(self):
        """Is executed when the Updater cog is unloaded"""
        self.update.stop()
        print("Updater unloaded")

    @tasks.loop(minutes=1)
    async def update(self):
        print("Searching for updates")
        result = subprocess.run(["git","pull","origin","main"],capture_output=True,text=True)
        if "up to date" in result.stdout:
            print("No updates found")
            return

        print("Update found!")

        while BotEvents.is_bot_used():
            await asyncio.sleep(10)
            print("Waiting for all actions to be finished...")

        # If the bot is connected to any voice channels, disconnect from them
        for guild in self.bot.guilds:
            if guild.voice_client:
                await guild.voice_client.disconnect(force=True)

        print("Now restarting bot")
        await self.bot.close()
        os.execl(sys.executable, sys.executable, *sys.argv)

    @update.before_loop
    async def before_track_time(self):
        """This will ensure that the TimeTracker only starts after the bot is ready."""
        await self.bot.wait_until_ready()