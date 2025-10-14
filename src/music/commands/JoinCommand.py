from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from discord.ext import commands

class JoinCommand(Command):
    """Command for letting the bot join the voice channel of the user who invoked the command."""
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.command(name="join",aliases=["j","Join","JOIN","joinChannel","JoinChannel","JOINCHANNEL","join_channel","Join_Channel","JOIN_CHANNEL"])
    async def execute(self, ctx):
        """
        Bot will join the voice channel of the user who invoked the command.
        If the user is not connected to a voice channel, an error message will be sent.
        :param ctx: The context of the command.
        """
        user_voice = ctx.author.voice
        bot_voice = ctx.voice_client

        if user_voice is None:
            await MessageManager.send_error_message(ctx.channel,"You are not connected to a voice channel.")
            return

        if bot_voice and bot_voice.channel == user_voice.channel:
            await MessageManager.send_error_message(ctx.channel,"Bot is already connected to your channel.")
            return

        if bot_voice and bot_voice.channel != user_voice.channel:
            await bot_voice.move_to(user_voice.channel)
            await MessageManager.send_message(ctx.channel,f"Moved to your channel: **{user_voice.channel.name}**")
            return

        await user_voice.channel.connect()
        await MessageManager.send_message(ctx.channel,f"Joined your channel: **{user_voice.channel.name}**")

    def help(self) -> str:
        """
        Help message for the command.
        :return: The help message.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}join` : Bot will join the voice channel of the user who invoked the command."