import discord

from common.BotUtils import BotUtils
from listbot.CommandHandler import CommandHandler
from discord.ext import commands

class ListCommands(commands.Cog):
    """
    A Discord cog that contains commands related to managing a list of games.
    This cog provides commands to add games.
    """

    def __init__(self,command_handler: CommandHandler):
        """
        Initializes the ListCommands cog.
        :param command_handler: An instance of CommandHandler to handle commands.
        """
        self.command_handler = command_handler

    @commands.command(name="add")
    async def add_game(self,ctx):
        """
        Command to add a game to the list.
        This command will create a button that, when clicked, will open a GameCreationModal to fill in
        the game details. The actual game adding will be handled by the GameCreationModal class.
        :param ctx: The context in which the command was invoked
        """
        await self.command_handler.add_command(ctx)

    @commands.command(name="update")
    async def update_game(self,ctx):
        """
        Command to update a game in the list.
        This command will create a button that, when clicked, will open a GameUpdateModal to update the existing game details.
        :param ctx: The context in which the command was invoked
        """
        await self.command_handler.update_command(ctx)

    @commands.command(name="replayed")
    async def replayed_game(self,ctx):
        """
        Command to mark a game as replayed.
        This command will check if the game exists in the database and if it does, it will
        mark the game as replayed.
        :param ctx: The context in which the command was invoked
        """
        await self.command_handler.replayed_hundred_percent_command(ctx, replay=True, hundred_percent=False)

    @commands.command(name="completed")
    async def hundred_percent_game(self,ctx):
        """
        Command to mark a game as completed (100%).
        This command will check if the game exists in the database and if it does, it will
        mark the game as completed.
        :param ctx: The context in which the command was invoked
        """
        await self.command_handler.replayed_hundred_percent_command(ctx, replay=False, hundred_percent=True)

    @commands.command(name="help")
    async def help_command(self, ctx):
        """
        Command to display the help message.
        This command will send a message with the available commands with their descriptions and syntax.
        :param ctx: The context in which the command was invoked
        """
        await self.command_handler.help_command(ctx)