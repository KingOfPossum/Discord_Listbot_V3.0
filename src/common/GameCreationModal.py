import discord

from common.GameEntry import GameEntry
from common.TimeUtils import TimeUtils
from database.Database import Database

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

    async def on_submit(self, interaction: discord.Interaction):
        """
        Called when the modal is submitted.
        This method will retrieve the values from the modal fields and store them in the database in other words
        it will create a new game entry in the database.
        :param interaction: the interaction in which the modal was submitted
        """
        game_name = self.children[0].value
        user = interaction.user.name
        date = self.game_entry.date if self.game_entry else TimeUtils.get_current_date_formated()
        console = self.children[1].value
        rating = self.children[2].value
        genre = self.children[3].value
        review = self.children[4].value

        game_entry = GameEntry(name=game_name,user=user,date=date,console=console,rating=int(rating),genre=genre,review=review,replayed=False,hundred_percent=False)
        self.database.put_game(game_entry,self.game_entry)

        print(game_entry)

        command_txt = "Updated" if self.game_entry else "Added"
        await interaction.response.send_message(f"**{command_txt} game : {game_name}**")