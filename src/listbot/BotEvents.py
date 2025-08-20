
from discord.ext import commands

from common.UserManager import UserManager


class BotEvents(commands.Cog):
    """
    A Discord cog that handles bot events.
    This cog listens for the `on_ready` event.
    """

    def __init__(self,bot: commands.Bot):
        """
        Initializes the BotEvents cog.
        :param bot: The bot instance to which this cog will be added.
        """
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event listener that is called when the bot is ready.
        This will print a message to the console indicating that the bot is ready.
        """
        print(f"Bot is ready! Logged in as {self.__bot.user.name} (ID: {self.__bot.user.id})")
        UserManager.init(self.__bot)