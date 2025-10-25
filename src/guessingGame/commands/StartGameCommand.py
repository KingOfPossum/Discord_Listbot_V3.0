import discord

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.ListDatabase import ListDatabase
from discord.ext import commands
from guessingGame.GameInstance import GameInstance
from guessingGame.commands.GameManager import GameManager

class StartGameCommand(Command):
    """
    Command for starting a guessing game.
    """
    def __init__(self, list_database:ListDatabase):
        self.list_database = list_database

    @commands.command(name="startGame")
    async def execute(self, ctx):
        """
        Starts a new guessing game. If there is already a game running you will be asked if you want to start a new one.
        :param ctx: The context of the command.
        """
        if UserManager.is_user_accepted(ctx.author.name):
           await MessageManager.send_message(ctx.channel,"You are not allowed to use this command!")

        if GameManager.game and GameManager.game.game_over:
            await MessageManager.send_message(ctx.channel,"There is already a guessing game running!")

            view = discord.ui.View()

            async def yes_callback(interaction: discord.Interaction):
                await self.start_new_game(ctx)
                await interaction.response.defer()

            yes_button = discord.ui.Button(label="Yes",style=discord.ButtonStyle.green)
            yes_button.callback = yes_callback

            view.add_item(yes_button)

            await MessageManager.send_message(ctx.channel,"Do you want to start a new game?",view=view)

        await self.start_new_game(ctx)

    def help(self) -> str:
        """
        Returns the help message.
        :return: The help message.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}startGame` - Starts a new guessing game.\n"

    async def start_new_game(self,ctx: commands.Context):
        GameManager.game = GameInstance(self.list_database, ctx)
        await MessageManager.send_message(ctx.channel,"Started a new game!")