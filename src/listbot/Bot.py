import os

import yaml
import discord

from discord.ext import commands

class Bot:
    config_data: dict = None
    intents: discord.Intents = discord.Intents.default()
    bot: commands.bot = None

    def __init__(self, command_prefix: str,config_path: str):
        self.create_resources_directory_if_not_exists()
        self.config_data = self.load_config(config_path)

        self.intents = self.set_intents()
        self.bot = commands.Bot(command_prefix=self.config_data['bot']['command_prefix'],intents=self.intents)

        @self.bot.event
        async def on_ready():
            print(f"Bot is ready! Logged in as {self.bot.user.name} (ID: {self.bot.user.id})")

    def run(self):
        api_key = self.config_data["bot"]["api_key"]

        try:
            self.bot.run(api_key)
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