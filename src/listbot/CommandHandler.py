
import discord

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