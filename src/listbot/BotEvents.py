from common.ConfigLoader import ConfigLoader
from common.Replies import Replies
from common.UserManager import UserManager
from discord.ext import commands

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
        self.replies = Replies("../resources/replies.yaml")

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event listener that is called when the bot is ready.
        This will print a message to the console indicating that the bot is ready.
        """
        print(f"Bot is ready! Logged in as {self.__bot.user.name} (ID: {self.__bot.user.id})")
        UserManager.init(self.__bot)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Event listener that is called when a message is sent in a channel.
        This is used to trigger non-command related events.
        """
        if not ConfigLoader.get_config().bot_replies:
            return

        if message.author == self.__bot.user:
            return
        if not ConfigLoader.get_config().bot_replies_to_links and message.content.startswith("https://"):
            return

        reply = self.replies.handle_message(message)
        if reply is not None:
            await message.reply(reply)