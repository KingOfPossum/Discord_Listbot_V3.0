from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord import VoiceClient
from discord.ext import commands
from voice.JoinResponse import JoinResponse

class JoinCommand(Command):
    """
    Command for letting bot join a channel.
    """
    @commands.command(name="join",aliases=["joinChannel","JOIN","Join","JoinChannel","JOINCHANNEL","joinchannel"])
    async def execute(self, ctx):
        """
        Executes the join command.
        If the bot is already in a voice channel, it moves to the user's channel.
        Otherwise, it joins the user's current voice channel.
        :param ctx: The context of the command.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are not allowed to use this command.")

        user_voice = ctx.author.voice
        bot_voice = ctx.voice_client

        status:JoinResponse = await JoinCommand.join(user_voice,bot_voice)

        match status:
            case JoinResponse.JOINED:
                await MessageManager.send_message(ctx.channel,f"Joined your voice channel `{user_voice.channel.name}`")
            case JoinResponse.MOVED:
                await MessageManager.send_message(ctx.channel,f"Moved to your voice channel `{user_voice.channel.name}`")
            case JoinResponse.USER_NOT_IN_VOICE:
                await MessageManager.send_error_message(ctx.channel,"You are not in a voice channel")
            case JoinResponse.ALREADY_IN_CHANNEL:
                await MessageManager.send_error_message(ctx.channel,"Bot is already in the voice channel")
            case JoinResponse.FAILED:
                await MessageManager.send_error_message(ctx.channel,"Failed to join your voice channel")

    def help(self) -> str:
        """
        Returns the help string for the join command.
        :return: Help string.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}join`: Lets the bot join your current voice channel\n"

    @staticmethod
    async def join(voice_client:VoiceClient,bot_voice_client:VoiceClient) -> JoinResponse:
        """
        Joins the voice channel.
        If bot is already in correct voice channel, does nothing.
        If the bot is in a different voice channel, moves to the user's channel.
        If the bot is not in any voice channel, joins the user's channel.
        :param voice_client: The voice client of the user.
        :param bot_voice_client: The voice client of the bot.
        :return: JoinResponse indicating the result of the operation.
        """
        try:
            if not voice_client:
                return JoinResponse.USER_NOT_IN_VOICE

            if voice_client and not bot_voice_client:
                await voice_client.channel.connect()
                return JoinResponse.JOINED

            if voice_client and bot_voice_client and voice_client.channel != bot_voice_client.channel:
                await bot_voice_client.move_to(voice_client.channel)
                return JoinResponse.MOVED

            return JoinResponse.ALREADY_IN_CHANNEL
        except Exception:
            return JoinResponse.FAILED