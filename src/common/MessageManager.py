import discord

class MessageManager:
    """
    A class to manage message sending and formatting in Discord featuring embedded messages.
    """

    @staticmethod
    async def send_embed_message(ctx, title: str, description: str, color: int = 0x00FF00, bot_message: bool = False):
        """
        Sends an embedded message to the context channel.
        :param ctx: The context in which the command was invoked.
        :param title: The title of the embedded message.
        :param description: The description of the embedded message.
        :param color: The color of the embedded message (default is green).
        """
        embed = discord.Embed(title=title, description=description, color=color)
        #ToDo: if bot_message is True, set the author to the bot's user with its avatar
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @staticmethod
    async def send_error_message(channel: discord.TextChannel, error_message: str):
        """
        Sends a formatted error message to the specified channel.
        :param channel: The channel where the error message will be sent.
        :param error_message: The error message to be sent.
        """
        await channel.send(f"```ml\nError:\n{error_message}```")