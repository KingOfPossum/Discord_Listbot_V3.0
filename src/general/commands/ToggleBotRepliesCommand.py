from common.ChannelManager import ChannelManager
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

class ToggleBotRepliesCommand(Command):
    """
    A command to toggle bot replies on or off for a specific channel.
    """
    @commands.command(name="toggleBotReplies")
    async def execute(self, ctx):
        """
        Toggles bot replies on or off for the current channel.
        If the channel is currently in the list of channels where bot replies are active, it will be removed.
        If the channel is not in the list, it will be added.
        :param ctx: The context of the command.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel, "You are Not Allowed to use this command")
            return

        bot_replies_channels = ChannelManager.bot_replies_channels or set()
        channel = ctx.message.channel

        if channel in bot_replies_channels:
            bot_replies_channels.remove(channel)
            await MessageManager.send_message(ctx.channel, "Bot replies have been deactivated successfully for this channel!")
        else:
            bot_replies_channels.add(channel)
            await MessageManager.send_message(ctx.channel, "Bot replies have been activated successfully for this channel!")

        print(bot_replies_channels)

        ConfigLoader.update("bot_replies_channels",[channel.id for channel in bot_replies_channels])

    def help(self) -> str:
        """
        Returns a help message for the command.
        :return: The help message as a string.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}toggleBotReplies`: Toggles bot replies on or off for the current channel.\n"