import discord

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.GameCreationModal import GameCreationModal
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.Database import Database
from discord.ext import commands

class UpdateCommand(Command):
    """
    Command to update an existing game in the list.
    """
    def __init__(self,database: Database):
        self.database = database

    @commands.command(name="update")
    async def execute(self, ctx):
        """
        Handles the 'update' command to update an existing game in the list.
        This command will check if the game exists in the database and if it does, it will
        create a button that, when clicked, will open a GameCreationModal to update the game details.
        If the game does not exist, it will send a message indicating that the game was not found.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        game_name = BotUtils.get_message_content(ctx.message)
        game = await BotUtils.game_exists(game_name,self.database,ctx=ctx)
        if game is None:
            return

        game_name, game_entry = game

        async def update_button_callback(interaction: discord.Interaction):
            modal = GameCreationModal(self.database, game_entry)
            await interaction.response.send_modal(modal)

        update_button = discord.ui.Button(label="Update Game",style=discord.ButtonStyle.blurple)
        update_button.callback = update_button_callback

        view = discord.ui.View()
        view.add_item(update_button)

        await ctx.send(view=view)

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}update` `gameName` - Update an existing Game\n"