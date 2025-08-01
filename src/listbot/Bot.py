import yaml
import discord

from discord.ext import commands

class Bot:
    config_data: dict = None
    intents: discord.Intents = discord.Intents.default()
    bot: commands.bot = None

    def __init__(self, command_prefix: str,config_path: str):
        self.intents = self.set_intents()
        self.bot = commands.Bot(command_prefix=command_prefix,intents=self.intents)
        self.config_data = self.load_config(config_path)

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
        with open(config_path,'r') as file:
            return yaml.safe_load(file)