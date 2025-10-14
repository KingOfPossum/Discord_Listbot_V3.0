from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager

class LeaveCommand(Command):
    """Command to make the b ot leave the voice channel."""
    def __init__(self, bot):
        self.bot = bot

    async def execute(self, ctx):
        """
        Bot will leave the voice channel it is currently in.
        If the user is not connected to a voice channel, he is not allowed to use this command and an error message will be sent.
        :param ctx: The context of the command.
        :return:
        """
        if ctx.author.voice is None:
            await MessageManager.send_error_message(ctx.channel, "You are not connected to a voice channel.")
            return

        await ctx.author.voice.channel.leave()

    def help(self) -> str:
        """
        Help message for the command.
        :return: The Help message.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}leave` : Bot will leave the voice channel it is currently in."
