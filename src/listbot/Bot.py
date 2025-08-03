import os

import yaml
import discord

from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands

class Bot:
    """
    A Discord bot that manages a list of games.
    """
    __config_data: dict = None
    __intents: discord.Intents = discord.Intents.default()
    __bot: commands.bot = None
    _databases:DatabaseCollection = None

    @property
    def databases(self) -> DatabaseCollection:
        """
        Returns the collection of databases used by the bot.
        :return: the DatabaseCollection instance containing the bot's databases.
        """
        return self._databases

    def __init__(self, command_prefix: str,config_path: str):
        """
        Initializes the bot.
        The bot will create a resources directory if it does not exist,
        and will load the configuration from the specified path.
        :param command_prefix: The prefix used for bot commands.
        :param config_path: The path to the configuration file for the bot.
        """
        self.create_resources_directory_if_not_exists()
        self.__config_data = self.load_config(config_path)
        self._databases = DatabaseCollection(self.__config_data['bot']['databases_folder_path'])

        self.__intents = self.set_intents()
        self.__bot = commands.Bot(command_prefix=self.__config_data['bot']['command_prefix'], intents=self.__intents)

        @self.__bot.event
        async def on_ready():
            print(f"Bot is ready! Logged in as {self.__bot.user.name} (ID: {self.__bot.user.id})")

    def run(self):
        """
        Runs the bot using the API key from the configuration file.
        This method will block until the bot is stopped.
        """
        api_key = self.__config_data["bot"]["api_key"]

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
    def load_config(config_path: str) -> dict:
        """
        Loads the configuration from the specified path.
        If the configuration file does not exist, it will be created with default values.
        :param config_path: The path to the configuration file.
        :return: The data loaded from the configuration file as a dictionary.
        """
        Bot.create_config_if_not_exists(config_path=config_path)

        with open(config_path,'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def create_resources_directory_if_not_exists():
        """
        Creates the resources directory if it does not exist.
        This directory is used to store the configuration file and is supposed to contain the databases(But can be changed in the config).
        """
        if not os.path.exists("../resources/"):
            print("Creating resources directory at: ../resources/")
            os.mkdir("../resources/")

    @staticmethod
    def create_config_if_not_exists(config_path: str):
        """
        Creates a configuration file at the specified path if it does not exist.
        The configuration file will contain default values.
        :param config_path: The path where the configuration file should be created.
        """
        if not os.path.exists(config_path):
            print(f"Creating configuration file at: {config_path}")
            with open(config_path, "w") as file:
                file.write("# Configuration file for the Discord bot\n")
                file.write("\n")
                file.write("# Discord bot configuration\n")
                file.write("bot:\n")
                file.write("  api_key:\n")
                file.write("  command_prefix: '%'\n")
                file.write("  databases_folder_path: '../resources/databases/'\n")
                file.write("  accepted_users:\n")