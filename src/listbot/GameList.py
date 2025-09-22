import discord

from common.EmojiCreator import EmojiCreator
from common.Emojis import Emojis
from common.GameEntry import GameEntry
from common.MessageManager import MessageManager
from database.ListDatabase import ListDatabase

class GameList:
    """
    This class represents a list of games for a user.
    """
    def __init__(self,database: ListDatabase,ctx: discord.Interaction,user: str = None):
        self.ctx = ctx
        self.user = user if user is not None else ctx.author.name
        self.database = database
        self.page = 1
        self.max_entries_per_page = 5
        self.games = self.database.get_all_game_entries_from_user(self.user)

    @staticmethod
    async def game_entry_to_list_entry(game_entry: GameEntry,guild) -> str:
        """
        Converts a GameEntry object to a string representation used in the list.
        Will add special emojis for completion and replayed status or for having a review.
        :param guild: The guild in which the list is being displayed. Used for fetching custom emojis.
        :param game_entry:
        :return: The string representation for the list
        """
        await EmojiCreator.create_console_emoji_if_not_exists(guild,game_entry.console)

        game_name = f"**{game_entry.name}**"
        replay_txt = "**(REPLAY)**" if game_entry.replayed else ""
        completion_txt = "**(100%)**" if game_entry.hundred_percent else ""
        console_txt = f"({Emojis.get_console_emoji(game_entry.console)})"
        rating_txt = f"Rating: **{game_entry.rating}**"
        date_txt = f"added on **{game_entry.date}**"
        review_txt = Emojis.REVIEW if len(game_entry.review) > 0 else ""

        return " ".join([game_name,replay_txt,completion_txt,console_txt,rating_txt,date_txt,review_txt])

    async def get_list_txt(self,guild) -> str:
        """
        Creates a string representing a list of games.
        It will only show the games for the current page,
        While only showing the set maximum number of entries per page.
        :param guild : The guild in which the list is being displayed. Used for fetching custom emojis.
        :return: The string representation of the game list for the current page.
        """
        start_index = (self.page - 1) * self.max_entries_per_page
        end_index = (self.page - 1) * self.max_entries_per_page + self.max_entries_per_page

        page_txt = f"**Page {self.page}/{self.number_of_pages()}**\n"
        number_games_txt = f"Number of games: **{len(self.games)}**"

        return page_txt + "\n".join([f"**{i + 1}.** {await self.game_entry_to_list_entry(self.games[i],guild)}" for i in range(start_index,end_index) if i < len(self.games)]) + "\n" + number_games_txt

    def next_page(self) -> int:
        """
        Moves to the next page of the game list.
        If the page gets out of bounds it will reset to the first page.
        :return: The next page number.
        """
        self.page += 1
        if (self.page - 1) * self.max_entries_per_page >= len(self.games):
            self.page = 1
        return self.page

    def previous_page(self) -> int:
        """
        Moves to the previous page of the game list.
        If the page gets out of bounds it will reset to the last page.
        :return: The previous page number.
        """
        self.page -= 1
        if self.page < 1:
            self.page = int(len(self.games) / self.max_entries_per_page)
        return self.page

    def number_of_pages(self) -> int:
        """
        Returns the number of pages in the game list.
        :return: The number of pages.
        """
        return (len(self.games) + self.max_entries_per_page - 1) // self.max_entries_per_page

    async def send_list(self,guild):
        """
        Sends the game list to the lists ctx channel.
        Will add two buttons for navigating through the pages.
        :param guild: The guild in which the list is being displayed. Used for fetching custom emojis.
        """
        if len(self.games) == 0:
            await MessageManager.send_error_message(self.ctx.channel,"you have No Games in your List")

        embed_title = f"**{self.ctx.author.display_name}'games**"
        embed_description = await self.get_list_txt(guild)
        embed = MessageManager.get_embed(title=embed_title,description=embed_description,user=self.ctx.author)

        async def next_callback(interaction: discord.Interaction):
            """
            Callback for the next button to show the next page of games.
            :param interaction: The interaction object for the button click.
            """
            self.next_page()
            embed.description = await self.get_list_txt(guild)
            await interaction.response.edit_message(embed=embed,view=view)

        async def previous_callback(interaction:  discord.Interaction):
            """
            Callback for the previous button to show the previous page of games.
            :param interaction: The interaction object for the button click.
            """
            self.previous_page()
            embed.description = await self.get_list_txt(guild)
            await interaction.response.edit_message(embed=embed,view=view)

        view = discord.ui.View()
        previous_button = discord.ui.Button(label="<",style=discord.ButtonStyle.green)
        next_button = discord.ui.Button(label=">",style=discord.ButtonStyle.blurple)

        previous_button.callback = previous_callback
        next_button.callback = next_callback

        view.add_item(previous_button)
        view.add_item(next_button)

        await MessageManager.send_message(self.ctx.channel,embed=embed,view=view)