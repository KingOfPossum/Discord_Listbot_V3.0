import discord

class GameCreationModal(discord.ui.Modal):
    """
    A modal for creating a new game entry.
    This modal will prompt the user to enter details about the game they want to add,
    including the name, console, rating, genre, and a review.
    """

    def __init__(self):
        """
        Initializes the GameCreationModal with fields for game details.
        """
        super().__init__(title="Add Game",timeout=None)

        self.add_item(discord.ui.TextInput(label="Name", placeholder="Enter the name of the game", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Console", placeholder="What console did you play on?", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Rating", placeholder="Put your rating here (0-100)", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Genre", placeholder="What Genre is the Game", required=False,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Review", placeholder="Your review", required=False,style=discord.TextStyle.paragraph))