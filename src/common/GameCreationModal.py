import discord

from common.ConfigLoader import ConfigLoader
from common.GameEntry import GameEntry
from common.MessageManager import MessageManager
from common.TimeUtils import TimeUtils
from database.ListDatabase import ListDatabase
from database.TokensDatabase import TokensDatabase
from listbot.Commands.CompletedCommand import CompletedCommand
from listbot.Commands.ReplayedCommand import ReplayedCommand
from listbot.Commands.ViewCommand import ViewCommand

class GameCreationModal(discord.ui.Modal):
    """
    A modal for creating a new game entry.
    This modal will prompt the user to enter details about the game they want to add,
    including the name, console, rating, genre, and a review.
    """
    def __init__(self,list_database: ListDatabase,token_database: TokensDatabase = None, game_entry: GameEntry = None):
        """
        Initializes the GameCreationModal with fields for game details.
        @param database: The database instance where the new gameEntry will be stored.
        """
        self.list_database = list_database
        self.token_database = token_database
        self.game_entry = game_entry

        self.added_token = False

        super().__init__(title="Add Game",timeout=None)

        self.add_item(discord.ui.TextInput(label="Name", default=game_entry.name if game_entry else "", placeholder="Enter the name of the game", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Console", default=game_entry.console if game_entry else "", placeholder="What console did you play on?", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Rating", default=str(game_entry.rating) if game_entry else "", placeholder="Put your rating here (0-100)", required=True,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Genre", default=game_entry.genre if game_entry else "", placeholder="What Genre is the Game", required=False,style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="Review", default=game_entry.review if game_entry else "", placeholder="Your review", required=False,style=discord.TextStyle.paragraph))

    async def _isvalid(self, interaction: discord.Interaction):
        """
        Checks if the input provided in the modal is valid.
        If the input is not valid, it will send an error message to the channel of the interaction.
        :param interaction: The interaction in which the modal was submitted.
        :return: True if the input is valid, False otherwise.
        """
        console = self.children[1].value

        try:
            rating = int(self.children[2].value)
        except ValueError:
            await interaction.response.defer()
            await MessageManager.send_error_message(interaction.channel,"please Provide a valid rating (0-100) as an number")
            return False

        if rating < 0 or rating > 100:
            await interaction.response.defer()
            await MessageManager.send_error_message(interaction.channel,"please Provide a rating between 0 and 100")
            return False
        if console not in ConfigLoader.get_config().consoles.keys():
            await interaction.response.defer()
            await MessageManager.send_error_message(interaction.channel,f"Console \"{console}\" is not valid, please provide a valid console")
            return False
        return True

    def _to_game_entry(self, user:str):
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

    async def _edit_message(self, interaction:discord.Interaction, new_game_entry:GameEntry, user:discord.User, view:discord.ui.View):
        """
        Edits the view message after pressing either the replayed or completed button.
        This method will update the message with the new game entry details and the updated embed.
        :param interaction: The interaction in which the button was pressed.
        :param new_game_entry: The updated GameEntry object after changing the replayed or completed status.
        :param user: The user who initiated the interaction, used to update the embed with their information.
        :param view: The view that contains the buttons for replayed and completed status.
        """
        changed_game_view_txt = ViewCommand.get_game_view_txt(new_game_entry)
        new_embed = MessageManager.get_embed(f"**{self.children[0]} {"(100%)" * new_game_entry.hundred_percent}**",
                                             description=changed_game_view_txt, user=user)

        if interaction.response.is_done():
            await interaction.followup.edit_message(embed=new_embed, view=view)
        else:
            await interaction.response.edit_message(embed=new_embed, view=view)

    def _get_game_view(self,interaction:discord.Interaction,game_entry: GameEntry) -> discord.ui.View:
        """
        Creates a view for the game entry.
        :return: The view containing buttons for replayed and completed status.
        """
        view = discord.ui.View()

        replayed_button = discord.ui.Button(label="Replay", style=discord.ButtonStyle.blurple)
        completed_button = discord.ui.Button(label="100%", style=discord.ButtonStyle.green)
        add_token_button = discord.ui.Button(label="Add Token", style=discord.ButtonStyle.red)

        async def replayed_callback(i: discord.Interaction):
            new_game_entry = await ReplayedCommand.change_replayed_status(game_name=game_entry.name,database=self.list_database,interaction=interaction)
            await self._edit_message(i, new_game_entry, interaction.user, view)

        async def completed_callback(i: discord.Interaction):
            new_game_entry = await CompletedCommand.change_completed_status(game_name=game_entry.name,database=self.list_database,interaction=interaction)
            await self._edit_message(i, new_game_entry, interaction.user, view)

        async def add_token_callback(i: discord.Interaction):
            if self.added_token:
                await i.response.defer()
                return

            await self.token_database.add_token(i.user.name,interaction=i)
            await MessageManager.send_message(i.channel,"Added Token")
            self.added_token = True
            i.response.defer()

        replayed_button.callback = replayed_callback
        completed_button.callback = completed_callback
        add_token_button.callback = add_token_callback

        view.add_item(replayed_button)
        view.add_item(completed_button)
        view.add_item(add_token_button)

        return view

    async def on_submit(self, interaction: discord.Interaction):
        """
        Called when the modal is submitted.
        This method will retrieve the values from the modal fields and store them in the database in other words
        it will create a new game entry in the database.
        :param interaction: the interaction in which the modal was submitted
        """
        if not await self._isvalid(interaction):
            return

        game_entry = self._to_game_entry(interaction.user.name)
        self.list_database.put_game(game_entry, self.game_entry)

        print(game_entry)

        game_view_txt = ViewCommand.get_game_view_txt(game_entry)
        embed = MessageManager.get_embed(f"**{self.children[0]} {"(100%)" * game_entry.hundred_percent}**",description=game_view_txt,user=interaction.user)

        view = self._get_game_view(interaction,game_entry)

        await MessageManager.send_message(channel=interaction.channel,embed=embed,view=view)
        await interaction.response.defer()