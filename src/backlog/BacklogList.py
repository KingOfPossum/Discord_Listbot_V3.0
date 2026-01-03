import discord

from common.BacklogEntry import BacklogEntry
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.BacklogDatabase import BacklogDatabase
from discord import User

class BacklogList:
    """
    A class for managing backlog lists messages for users.
    Each user has their own backlog list.
    """
    ENTRIES_PER_PAGE = 10

    def __init__(self,backlog_database:BacklogDatabase,user:User):
        self.backlog_database = backlog_database
        self.user = user
        self.page = 1
        self.entries = sorted(self.backlog_database.get_all_entries(user.name),key=lambda entry: entry.name.lower())
        self.view = discord.ui.View()

    def number_of_pages(self) -> int:
        """
        Returns the number of pages in the game list.
        :return: The number of pages.
        """
        return (len(self.entries) + BacklogList.ENTRIES_PER_PAGE - 1) // BacklogList.ENTRIES_PER_PAGE

    def entry_to_list_entry(self,entry:BacklogEntry):
        """
        Converts a BacklogEntry object to a string representation for display in the backlog list.
        :param entry: The BacklogEntry object to convert.
        :return: The string representation of the backlog entry.
        """
        return f"**{entry.name}** (recommended by: *{entry.recommended_by}*)" if entry.recommended_by else f"**{entry.name}**"

    def get_list_txt(self) -> str:
        """
        Creates a string representing the backlog list for the current page.
        :return: The string representation of the backlog list for the current page.
        """
        start_index = (self.page - 1) * BacklogList.ENTRIES_PER_PAGE
        end_index = (self.page - 1) * BacklogList.ENTRIES_PER_PAGE + BacklogList.ENTRIES_PER_PAGE

        page_txt = f"**Page {self.page}/{self.number_of_pages()}**\n"
        number_entries_txt = f"Number of entries: **{len(self.entries)}**"

        return page_txt + "\n".join([f"- {self.entry_to_list_entry(self.entries[i])}" for i in range(start_index,end_index) if i < len(self.entries)]) + f"\n{number_entries_txt}"

    async def prev_page(self,interaction):
        """
        Moves to the previous page of the backlog list and updates the message.
        If the page gets out of bounds it will reset to the last page.
        :param interaction: The interaction that triggered the page change.
        """
        self.page -= 1
        if self.page < 1:
            self.page = int(len(self.entries) / BacklogList.ENTRIES_PER_PAGE)

        new_embed = MessageManager.get_embed(title=f"**{self.user.display_name}'s Backlog**",description=self.get_list_txt(), user=self.user)
        await interaction.response.edit_message(embed=new_embed,view=self.view)

    async def next_page(self,interaction):
        """
        Moves to the next page of the backlog list and updates the message.
        If the page gets out of bounds it will reset to the first page.
        :param interaction: the interaction that triggered the page change.
        """
        self.page += 1
        if (self.page - 1) * BacklogList.ENTRIES_PER_PAGE >= len(self.entries):
            self.page = 1

        new_embed = MessageManager.get_embed(title=f"**{self.user.display_name}'s Backlog**",description=self.get_list_txt(), user=self.user)
        await interaction.response.edit_message(embed=new_embed,view=self.view)

    async def send_list(self,channel):
        """
        Sends the backlog list to the specified channel.
        :param channel: The channel to send the backlog list to.
        :return:
        """
        embed = MessageManager.get_embed(title=f"**{self.user.display_name}'s Backlog**",description=self.get_list_txt(),user=self.user)

        previous_button = discord.ui.Button(label="<",style=discord.ButtonStyle.green)
        previous_button.callback = self.prev_page

        next_button = discord.ui.Button(label=">",style=discord.ButtonStyle.blurple)
        next_button.callback = self.next_page

        self.view.add_item(previous_button)
        self.view.add_item(next_button)

        for user in UserManager.accepted_users:
            if user.name not in self.backlog_database.users_with_backlog():
                continue

            user_button = discord.ui.Button(label=user.display_name,style=discord.ButtonStyle.gray)

            async def user_callback(interaction,member:User=user):
                self.entries = sorted(self.backlog_database.get_all_entries(member.name),key = lambda entry: entry.name.lower())
                self.user = member
                self.page = 1

                new_embed = MessageManager.get_embed(title=f"**{self.user.display_name}'s Backlog**",description=self.get_list_txt(), user=self.user)
                await interaction.response.edit_message(embed=new_embed,view=self.view)

            user_button.callback = user_callback
            self.view.add_item(user_button)

        await MessageManager.send_message(channel,embed=embed,view=self.view)