
import discord

from common.GameCreationModal import GameCreationModal

class CommandHandler:
    """
    A class that handles commands related to game management in a Discord bot.
    This class provides a static method to handle the 'add' command, which will prompt the user with a modal to fill in game details.
    """

    @staticmethod
    async def add_command(interaction: discord.Interaction):
        """
        Handles the 'add' command to add a game to the list.
        Will show the user a modal to fill in the game details.
        :param interaction: The interaction in which the modal will be send.
        """
        modal = GameCreationModal()
        await interaction.response.send_modal(modal)