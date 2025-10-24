from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from discord.ext import commands

class LeaveCommand(Command):
    """
    Command for letting bot leave a channel.
    """
    @commands.command(name="leave",aliases=["Leave","LEAVE","leaveChannel","leavechannel","LEAVECHANNEL","leave_channel","Leave_Channel","LEAVE_Channel"])
    async def execute(self, ctx):
        """
        Executes the leave command.
        Makes the bot leave the current voice channel.
        If the bot is in no channel an error message will be sent.
        :param ctx: The context of the command.
        """
        bot_voice = ctx.voice_client

        if not bot_voice:
            await MessageManager.send_error_message(ctx.channel,"The bot is not in a voice channel.")
            return

        await bot_voice.disconnect()
        await MessageManager.send_message(ctx.channel,"Left the voice channel!")

    def help(self) -> str:
        """
        Returns the help string for the leave command.
        :return: Help string.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}leave` : Lets the bot leave the current voice channel\n"