import discord

from common.TimeUtils import TimeUtils
from database.Database import Database

class GameCreationModal(discord.ui.Modal):
    """
    A modal for creating a new game entry.
    This modal will prompt the user to enter details about the game they want to add,
    including the name, console, rating, genre, and a review.
    """

    def __init__(self,database: Database):
        """
        Initializes the GameCreationModal with fields for game details.
        @param database: The database instance where the new gameEntry will be stored.
        """
        self.database = database

        super().__init__(title="Add Game",timeout=None)

        self.add_item(discord.ui.TextInput(label="Name", placeholder="Enter the name of the game", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Console", placeholder="What console did you play on?", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Rating", placeholder="Put your rating here (0-100)", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Genre", placeholder="What Genre is the Game", required=False,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Review", placeholder="Your review", required=False,style=discord.TextStyle.paragraph))

    async def on_submit(self, interaction: discord.Interaction):
        """
        Called when the modal is submitted.
        This method will retrieve the values from the modal fields and store them in the database in other words
        it will create a new game entry in the database.
        :param interaction: the interaction in which the modal was submitted
        """
        game_name = self.children[0].value
        user = interaction.user.name
        data = TimeUtils.get_current_date_formated()
        console = self.children[1].value
        rating = self.children[2].value
        genre = self.children[3].value
        review = self.children[4].value

        self.database.sql_execute(f"INSERT INTO {self.database.table_name} (name, user, date, console, rating, genre, review) VALUES (?, ?, ?, ?, ?, ?, ?)",(game_name, user, data, console, rating, genre, review))

        await interaction.response.defer()