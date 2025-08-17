import discord

from common.ConfigLoader import ConfigLoader
from common.GameEntry import GameEntry
from common.MessageManager import MessageManager
from common.TimeUtils import TimeUtils
from database.Database import Database
from listbot.Commands.ViewCommand import ViewCommand


class GameCreationModal(discord.ui.Modal):
    """
    A modal for creating a new game entry.
    This modal will prompt the user to enter details about the game they want to add,
    including the name, console, rating, genre, and a review.
    """

    def __init__(self,database: Database, game_entry: GameEntry = None):
        """
        Initializes the GameCreationModal with fields for game details.
        @param database: The database instance where the new gameEntry will be stored.
        """
        self.database = database
        self.game_entry = game_entry

        super().__init__(title="Add Game",timeout=None)

        self.add_item(discord.ui.TextInput(label="Name", default=game_entry.name if game_entry else "", placeholder="Enter the name of the game", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Console", default=game_entry.console if game_entry else "", placeholder="What console did you play on?", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Rating", default=str(game_entry.rating) if game_entry else "", placeholder="Put your rating here (0-100)", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Genre", default=game_entry.genre if game_entry else "", placeholder="What Genre is the Game", required=False,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Review", default=game_entry.review if game_entry else "", placeholder="Your review", required=False,style=discord.TextStyle.paragraph))

    async def __isvalid(self,interaction: discord.Interaction):
        """
        Checks if the input provided in the modal is valid.
        If the input is not valid, it will send an error message to the channel of the interaction.
        :param interaction: The interaction in which the modal was submitted.
        :return: True if the input is valid, False otherwise.
        """
        console = self.children[1].value
        rating = int(self.children[2].value)

        if rating < 0 or rating > 100:
            await interaction.response.defer()
            await MessageManager.send_error_message(interaction.channel,"please Provide a rating between 0 and 100")
            return False
        if console not in ConfigLoader.get_config().consoles.keys():
            await interaction.response.defer()
            await MessageManager.send_error_message(interaction.channel,f"Console \"{console}\" is not valid, please provide a valid console")
            return False
        return True

    def __to_game_entry(self,user:str):
        """
        Converts the modal input fields into a GameEntry object.
        This method will create a new GameEntry object with the values provided in the modal fields.
        :param user: The username of the user who is creating the game entry.
        :return: The created GameEntry object with the provided values.
        """
        game_name = self.children[0].value
        date = self.game_entry.date if self.game_entry else TimeUtils.get_current_date_formated()
        console = self.children[1].value
        rating = int(self.children[2].value)
        genre = self.children[3].value
        review = self.children[4].value

        return GameEntry(name=game_name, user=user, date=date, console=console, rating=rating, genre=genre,
                               review=review, replayed=False, hundred_percent=False)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Called when the modal is submitted.
        This method will retrieve the values from the modal fields and store them in the database in other words
        it will create a new game entry in the database.
        :param interaction: the interaction in which the modal was submitted
        """
        if not await self.__isvalid(interaction):
            return

        game_entry = self.__to_game_entry(interaction.user.name)
        self.database.put_game(game_entry, self.game_entry)

        print(game_entry)

        game_view_txt = ViewCommand.get_game_view_txt(game_entry)
        embed = MessageManager.get_embed(f"**{self.children[0]} {"(100%)" * game_entry.hundred_percent}**",description=game_view_txt,user=interaction.user)

        await MessageManager.send_message(interaction=interaction,embed=embed)