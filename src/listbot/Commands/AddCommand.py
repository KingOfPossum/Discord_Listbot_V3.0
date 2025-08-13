import discord

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.GameCreationModal import GameCreationModal
from database.Database import Database
from discord.ext import commands

class AddCommand(Command):
    """
    Command to add a new game to the list.
    This command will create a button that, when clicked, will open a GameCreationModal to
    fill in the game details.
    """
    def __init__(self,database: Database):
        self.database = database

    @commands.command(name="add")
    async def execute(self, ctx):
        """
        Handles the 'add' command to add a game to the list.
        Will show the user a modal to fill in the game details.
        :param ctx: The context in which the command was invoked
        """
        add_button = discord.ui.Button(label="Add Game", style=discord.ButtonStyle.green)
        add_button.callback = lambda interaction: interaction.response.send_modal(
            GameCreationModal(self.database))

        view = discord.ui.View()
        view.add_item(add_button)

        await ctx.send(view=view)

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}add` - Add a new game to the list\n"