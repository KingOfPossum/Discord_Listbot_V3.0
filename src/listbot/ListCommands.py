import discord

from listbot.CommandHandler import CommandHandler
from discord.ext import commands

class ListCommands(commands.Cog):
    """
    A Discord cog that contains commands related to managing a list of games.
    This cog provides commands to add games.
    """

    @commands.command(name="add")
    async def add_game(self,ctx):
        """
        Command to add a game to the list.
        This command will create a button that, when clicked, will open a GameCreationModal to fill in
        the game details. The actual game adding will be handled by the GameCreationModal class.
        :param ctx: The context in which the command was invoked
        """
        add_button = discord.ui.Button(label="Add Game", style=discord.ButtonStyle.green)
        add_button.callback = CommandHandler.add_command

        view = discord.ui.View()
        view.add_item(add_button)

        await ctx.send(view=view)