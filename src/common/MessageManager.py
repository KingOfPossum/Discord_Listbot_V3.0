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
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)