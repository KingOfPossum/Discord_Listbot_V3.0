from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

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

        if not user_voice:
            await MessageManager.send_error_message(ctx.channel,"You need to be in a voice channel to use this command.")
            return

        if not bot_voice:
            await user_voice.channel.connect()
            await MessageManager.send_message(ctx.channel,f"Joined channel **{user_voice.channel.name}** (where the sigmas at?)!")
            return

        if user_voice.channel == bot_voice.channel:
            await MessageManager.send_error_message(ctx.channel,"The bot is already in your voice channel.")
            return

        if user_voice and bot_voice and user_voice.channel != bot_voice.channel:
            await bot_voice.move_to(user_voice.channel)
            await MessageManager.send_message(ctx.channel,f"Moved to channel **{user_voice.channel.name}**!")
            return


    def help(self) -> str:
        """
        Returns the help string for the join command.
        :return: Help string.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}join`: Lets the bot join your current voice channel\n"