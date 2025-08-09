import asyncio
import discord
import os

from common.ConfigLoader import ConfigLoader
from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands
from listbot.BotEvents import BotEvents
from listbot.ListCommands import ListCommands
from listbot.CommandHandler import CommandHandler

class Bot:
    """
    A Discord bot that manages a list of games.
    """
    _databases:DatabaseCollection = None
    command_prefix: str = None

    @property
    def databases(self) -> DatabaseCollection:
        """
        Returns the collection of databases used by the bot.
        :return: the DatabaseCollection instance containing the bot's databases.
        """
        return self._databases

    def __init__(self):
        """
        Initializes the bot.
        The bot will create a resources directory if it does not exist,
        and will load the configuration from the specified path.
        """
        self.create_resources_directory_if_not_exists()

        self.__config_data = ConfigLoader.load()
        print(self.__config_data)

        self._databases = DatabaseCollection(self.__config_data.database_folder_path)
        self._command_handler = CommandHandler(self.databases)

        self.command_prefix = self.__config_data.command_prefix

        self.__intents = self.set_intents()
        self.__bot = commands.Bot(command_prefix=self.command_prefix, intents=self.__intents)

        asyncio.run(self.register_events())
        asyncio.run(self.register_commands())

    async def register_events(self):
        """Registers the bot events cog."""
        await self.__bot.add_cog(BotEvents(self.__bot))
        print("Registered BotEvents cog.")

    async def register_commands(self):
        """Registers the list commands cog."""
        await self.__bot.add_cog(ListCommands(self._command_handler))
        print("Registered ListCommands cog.")

    def run(self):
        """
        Runs the bot using the API key from the configuration file.
        This method will block until the bot is stopped.
        """
        api_key = self.__config_data.api_key

        try:
            self.__bot.run(api_key)
        finally:
            input("Press any key to exit...")

    @staticmethod
    def set_intents() -> discord.Intents:
        """
        Sets the intents for the bot.
        This method enables the message content intent, which is required for the bot to read message content.
        :return: New discord.Intents object with set intents.
        """
        intents = discord.Intents.default()
        intents.message_content = True

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