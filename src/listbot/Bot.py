import asyncio
import discord
import os

from common.ConfigLoader import ConfigLoader
from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands
from general.Commands.GeneralCommands import GeneralCommands
from listbot.BotEvents import BotEvents
from listbot.Commands.ListCommands import ListCommands
from tokenSystem.commands.TokenCommands import TokenCommands

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

        self.__config_data = ConfigLoader.get_config()
        print(self.__config_data)

        self._databases = DatabaseCollection(self.__config_data.database_folder_path)
        self._databases.init_list_database()
        self._databases.init_tokens_database()

        self.command_prefix = self.__config_data.command_prefix

        self.__intents = self.set_intents()
        self.__bot = commands.Bot(command_prefix=self.command_prefix, intents=self.__intents)

        self.__bot.remove_command('help')
        self.list_commands = ListCommands(self._databases)
        self.general_commands = GeneralCommands()
        self.tokens_commands = TokenCommands(self._databases)

        asyncio.run(self.register_events())
        asyncio.run(self.register_commands())

    async def register_events(self):
        """Registers the bot events cog."""
        await self.__bot.add_cog(BotEvents(self.__bot,self._databases))
        print("Registered BotEvents cog.")

    async def register_commands(self):
        """Registers the list commands cogs."""
        await self.list_commands.register(self.__bot)
        await self.general_commands.register(self.__bot)
        await self.tokens_commands.register(self.__bot)
        print("Cogs:", list(self.__bot.cogs.keys()))
        print("Commands:", [c.name for c in self.__bot.commands])
        print()

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
        intents.members = True
        intents.guilds = True
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