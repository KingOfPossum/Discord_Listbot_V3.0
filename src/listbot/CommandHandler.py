import discord

from common.BotUtils import BotUtils
from common.GameCreationModal import GameCreationModal
from database.DatabaseCollection import DatabaseCollection

class CommandHandler:
    """
    A class that handles commands related to game management in a Discord bot.
    This class provides a static method to handle the 'add' command, which will prompt the user with a modal to fill in game details.
    """

    def __init__(self,databases: DatabaseCollection):
        self.databases = databases

    async def add_command(self,interaction: discord.Interaction):
        """
        Handles the 'add' command to add a game to the list.
        Will show the user a modal to fill in the game details.
        :param interaction: The interaction in which the modal will be send.
        """
        modal = GameCreationModal(self.databases.list_database)
        await interaction.response.send_modal(modal)

    async def update_command(self, ctx: discord.Interaction):
        """
        Handles the 'update' command to update an existing game in the list.
        This command will check if the game exists in the database and if it does, it will
        create a button that, when clicked, will open a GameCreationModal to update the game details.
        If the game does not exist, it will send a message indicating that the game was not found.
        :param ctx: The context in which the command was invoked
        """

        game_name = BotUtils.get_message_content(ctx.message)
        game_entry = self.databases.list_database.get_game_entry(game_name, ctx.author.name)

        if game_entry is None:
            await ctx.send("**Game not found!**")
            return
        else:
            print(game_entry)

        async def update_button_callback(interaction: discord.Interaction):
            modal = GameCreationModal(self.databases.list_database, game_entry)
            await interaction.response.send_modal(modal)

        update_button = discord.ui.Button(label="Update Game",style=discord.ButtonStyle.blurple)
        update_button.callback = update_button_callback

        view = discord.ui.View()
        view.add_item(update_button)

        await ctx.send(view=view)