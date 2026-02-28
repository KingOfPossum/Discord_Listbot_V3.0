import discord
import os

from backlog.commands.BacklogCommands import BacklogCommands
from common.BootLoop import BotLoop
from common.ConfigLoader import ConfigLoader
from common.Wrapper import Wrapper
from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands
from general.commands.GeneralCommands import GeneralCommands
from listbot.BotEvents import BotEvents
from listbot.Updater import Updater
from listbot.commands.ListCommands import ListCommands
from timeTracking.TimeTracker import TimeTracker
from timeTracking.commands.TimeTrackingCommands import TimeTrackingCommands
from tokenSystem.commands.TokenCommands import TokenCommands
from voice.DownloadManager import DownloadManager
from voice.MusicManager import MusicManager
from voice.SongUpdater import SongUpdater
from voice.commands.VoiceCommands import VoiceCommands

class Bot(commands.Bot):
    """
    A Discord bot that manages a list of games.
    """
    _databases:DatabaseCollection = None
    command_prefix: str = None

    def __init__(self):
        """
        Initializes the bot.
        The bot will create a resources directory if it does not exist,
        and will load the configuration from the specified path.
        """
        self.create_resources_directory_if_not_exists()

        self.__config_data = ConfigLoader.get_config()
        print(self.__config_data)

        Wrapper.init()

        self._databases = DatabaseCollection(self.__config_data.database_folder_path)
        self._databases.init_databases()

        self.music_manager = MusicManager(self.__config_data.music_folder_path)

        self.command_prefix = self.__config_data.command_prefix

        self.__intents = self.set_intents()
        super().__init__(command_prefix=self.command_prefix, intents=self.__intents)

        self.remove_command('help')
        self.backlog_commands = BacklogCommands()
        self.list_commands = ListCommands()
        self.general_commands = GeneralCommands()
        self.tokens_commands = TokenCommands()
        self.time_commands = TimeTrackingCommands()
        self.voice_commands = VoiceCommands()

        DownloadManager.init_options()

    async def setup_hook(self):
        """A setup hook that is called when the bot is ready."""
        BotLoop.loop = self.loop
        await self.register_cogs()

    async def register_cogs(self):
        """Registers all the cogs for the bot."""
        await self.register_events()
        await self.register_commands()
        await self.register_tasks()

    async def register_events(self):
        """Registers the bot events cog."""
        await self.add_cog(BotEvents(self))
        print("Registered BotEvents cog.")

    async def register_commands(self):
        """Registers the list commands cogs."""
        await self.list_commands.register(self)
        await self.general_commands.register(self)
        await self.tokens_commands.register(self)
        await self.time_commands.register(self)
        await self.voice_commands.register(self)
        await self.backlog_commands.register(self)
        print("Cogs:", list(self.cogs.keys()))
        print("Commands:", [c.name for c in self.commands])
        print()

    async def register_tasks(self):
        """Registers the bot tasks."""
        await self.add_cog(TimeTracker(self))
        await self.add_cog(SongUpdater(self))

        if ConfigLoader.get_config().automatic_updates:
            await self.add_cog(Updater(self))

    def run_bot(self):
        """
        Runs the bot using the API key from the configuration file.
        This method will block until the bot is stopped.
        """
        api_key = self.__config_data.api_key

        try:
            super().run(api_key)
        finally:
            print("Shutting down bot.")

    @staticmethod
    def set_intents() -> discord.Intents:
        """
        Sets the intents for the bot.
        This method enables the message content intent, which is required for the bot to read message content.
        :return: New discord.Intents object with set intents.
        """
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.presences = True
        return intents

    @staticmethod
    def create_resources_directory_if_not_exists():
        """
        Creates the resources directory if it does not exist.
        This directory is used to store the configuration file and is supposed to contain the databases(But can be changed in the config).
        """
        if not os.path.exists("../resources/"):
            print("Creating resources directory at: ../resources/")
            os.mkdir("../resources/")