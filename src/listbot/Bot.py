import os

import yaml
import discord

from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands

class Bot:
    __config_data: dict = None
    __intents: discord.Intents = discord.Intents.default()
    __bot: commands.bot = None
    _databases:DatabaseCollection = DatabaseCollection("../resources/databases/")

    @property
    def databases(self) -> DatabaseCollection:
        return self._databases

    def __init__(self, command_prefix: str,config_path: str):
        self.create_resources_directory_if_not_exists()
        self.__config_data = self.load_config(config_path)

        self.__intents = self.set_intents()
        self.__bot = commands.Bot(command_prefix=self.__config_data['bot']['command_prefix'], intents=self.__intents)

        @self.__bot.event
        async def on_ready():
            print(f"Bot is ready! Logged in as {self.__bot.user.name} (ID: {self.__bot.user.id})")

    def run(self):
        api_key = self.__config_data["bot"]["api_key"]

        try:
            self.__bot.run(api_key)
        finally:
            input("Press any key to exit...")

    @staticmethod
    def set_intents() -> discord.Intents:
        intents = discord.Intents.default()
        intents.message_content = True

        return intents

    @staticmethod
    def load_config(config_path: str) -> dict:
        Bot.create_config_if_not_exists(config_path=config_path)

        with open(config_path,'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def create_resources_directory_if_not_exists():
        if not os.path.exists("../resources/"):
            os.mkdir("../resources/")

    @staticmethod
    def create_config_if_not_exists(config_path: str):
        if not os.path.exists(config_path):
            with open(config_path, "w") as file:
                file.write("# Configuration file for the Discord bot\n")
                file.write("\n")
                file.write("# Discord bot configuration\n")
                file.write("bot:\n")
                file.write("  api_key:\n")
                file.write("  command_prefix: '%'\n")
                file.write("  accepted_users:\n")