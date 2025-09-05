import discord

from common.ConfigLoader import ConfigLoader

class ChannelManager:
    bot_replies_channels: set[discord.TextChannel] = set()

    @staticmethod
    async def init(bot):
        bot_replies_channels_config = ConfigLoader.get_config().bot_replies_channels

        if bot_replies_channels_config is None:
            return
        elif bot_replies_channels_config == {"all"}:
            ChannelManager.bot_replies_channels = {channel for guild in bot.guilds for channel in guild.channels if channel.type == discord.ChannelType.text}
        else:
            for channel in bot_replies_channels_config:
                ChannelManager.bot_replies_channels.add(await bot.fetch_channel(channel))

        print(f"ChannelManager initialized with bot replies channels: {ChannelManager.bot_replies_channels}\n")

    @staticmethod
    def is_channel_accepted(channel: discord.TextChannel) -> bool:
        """
        Checks if a channel is accepted to use the bot.
        :param channel: The channel to check.
        :return: True if the channel is accepted, False otherwise.
        """
        for accepted_channel in ChannelManager.bot_replies_channels:
            if accepted_channel.id == channel.id:
                return True

        return False