import discord

class MessageManager:
    """
    A class to manage message sending and formatting in Discord featuring embedded messages.
    """
    @staticmethod
    def get_embed(title:str,description:str,color:int = 0x00FF00,user:discord.User = None) -> discord.Embed:
        """
        Creates an embed with the given title and description.
        If user is provided it will set the author of the embed to the user's display name and avatar.
        :param title: The title of the embed.
        :param description: The description of the embed.
        :param color: The color of the embed (default is green).
        :param user: The user to set as the author of the embed (optional).
        :return: The created embed object.
        """
        embed = discord.Embed(title=title, description=description, color=color)
        if user:
            embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        return embed

    @staticmethod
    async def send_message(ctx: discord.Interaction = None, interaction: discord.Interaction = None,message: str = "", embed: discord.Embed = None, view: discord.ui.View = None):
        """
        Sends a message to either a contexts or an interactions channel.
        If an embed is provided, it will be sent with the message.
        If an view is provided, it will be added to the message.
        :param ctx: The context in which the command was invoked.
        :param interaction: The interaction in which the command was invoked.
        :param message: The message to be sent.
        :param embed: An optional embed to be sent with the message.
        :param view: An optional view to be added to the message.
        """
        if not (ctx or interaction):
            raise ValueError("Either ctx or interaction must be provided to send a message.")

        kwargs = {"content": message}
        if embed:
            kwargs["embed"] = embed
        if view:
            kwargs["view"] = view

        if ctx:
            await ctx.send(**kwargs)
        else:
            if interaction.response.is_done():
                await interaction.followup.send(**kwargs)
            else:
                await interaction.response.send_message(**kwargs)

    @staticmethod
    async def send_error_message(channel: discord.TextChannel, error_message: str):
        """
        Sends a formatted error message to the specified channel.
        :param channel: The channel where the error message will be sent.
        :param error_message: The error message to be sent.
        """
        await channel.send(f"```ml\nError:\n{error_message}```")