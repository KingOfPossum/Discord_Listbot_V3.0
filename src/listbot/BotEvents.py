import discord

from common.ChannelManager import ChannelManager
from common.ConfigLoader import ConfigLoader
from common.Replies import Replies
from common.UserManager import UserManager
from discord.ext import commands

class BotEvents(commands.Cog):
    """
    A Discord cog that handles bot events.
    This cog listens for the `on_ready` event.
    """
    _active_uses:int = 0 # Amount of interactions/commands that are currently active

    def __init__(self,bot: commands.Bot):
        """
        Initializes the BotEvents cog.
        :param bot: The bot instance to which this cog will be added.
        """
        self.__bot = bot
        self.replies = Replies("../resources/replies.yaml")

        self.__bot.before_invoke(self._before_invoke)
        self.__bot.after_invoke(self._after_invoke)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event listener that is called when the bot is ready.
        This will print a message to the console indicating that the bot is ready.
        """
        print(f"Bot is ready! Logged in as {self.__bot.user.name} (ID: {self.__bot.user.id})\n")
        UserManager.init(self.__bot)
        await ChannelManager.init(self.__bot)
        #self.databases.init_tokens_database()

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Event listener that is called when a message is sent in a channel.
        This is used to trigger non-command related events.
        """
        if not ConfigLoader.get_config().bot_replies:
            return

        if not ChannelManager.is_channel_accepted(message.channel):
            return
        if message.author == self.__bot.user:
            return
        if not ConfigLoader.get_config().bot_replies_to_links and message.content.startswith("https://"):
            return
        if message.content.startswith(ConfigLoader.get_config().command_prefix):
            return
        if message.author not in UserManager.bot_replies_users:
            return

        reply = self.replies.handle_message(message)
        if reply is not None:
            await message.reply(reply)

    @classmethod
    def start_action(cls,action:str = ""):
        """
        Should be called at the beginning of each action.
        :param action: The name of the action for better logging
        """
        cls._active_uses += 1
        print(f"Started Action ({action})! Currently active uses: {str(cls._active_uses)}")

    @classmethod
    def end_action(cls,action:str = ""):
        """
        Should be called at the end of each action.
        :param action: The name of the action for better logging
        :return:
        """
        cls._active_uses -= 1
        print(f"Ended Action ({action})! Currently active uses: {str(cls._active_uses)}")

    async def _before_invoke(self,ctx: commands.Context):
        """
        Should be called whenever a command is invoked or something like a modal has been opened.
        Is meant for keeping track of how many things are currently being processed.
        Meaning for commands or interactions that are instantly executed this method should not be called as they dont need processing.
        """
        self.start_action(ctx.command.name)

    async def _after_invoke(self,ctx: commands.Context):
        """
        Should be called whenever a command has finished or something like a modal has been closed.
        Is meant for keeping track of how many things are currently being processed.
        Meaning for commands or interactions that are instantly executed this method should not be called as they dont need processing.
        """
        self.end_action(ctx.command.name)

    @staticmethod
    def is_bot_used():
        """
        Is anyone currently using the bot. In other words are there any unfinished commands or interactions.
        :return: True if the bot is currently being used, False otherwise.
        """
        return BotEvents._active_uses != 0

    @commands.Cog.listener()
    async def on_interaction(self,interaction: discord.Interaction):
        self.start_action("Interaction")

        action_type = ""
        try:
            if interaction.type == discord.InteractionType.component:
                custom_id = interaction.data.get("custom_id")
                action_type = f"button/dropdown <{custom_id}>"
            elif interaction.type == discord.InteractionType.modal_submit:
                custom_id = interaction.data.get("custom_id")
                action_type = f"modal_submit <{custom_id}>"
        finally:
            self.end_action(action_type)