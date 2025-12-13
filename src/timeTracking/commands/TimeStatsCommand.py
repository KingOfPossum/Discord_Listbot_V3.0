import discord

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.TimeEntry import TimeEntry
from common.TimeUtils import TimeUtils
from common.UserManager import UserManager
from database_.TimeDatabase import TimeDatabase
from discord.ext import commands

class TimeStatsCommand(Command):
    """
    Command to get time tracking statistics.
    """
    ENTRIES_PER_PAGE = 5

    def __init__(self, time_database: TimeDatabase):
        self.time_database = time_database

    @commands.command(name="timeStats", aliases=["timestats", "TimeStats", "TIMESTATS", "ts", "TS"])
    async def execute(self, ctx):
        """
        Executes the timeStats command.
        This command retrieves and displays the time tracking statistics for the user who invoked the command.
        :param ctx: The context of the command invocation.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        entries = sorted(self.time_database.get_all_time_entries(user=ctx.author.name),key=lambda t: t.time_spent,reverse=True)

        if not entries or len(entries) == 0:
            await MessageManager.send_error_message(ctx.channel,"You have no time statistics yet.")
            return

        page_amount = (len(entries) + self.ENTRIES_PER_PAGE - 1) // self.ENTRIES_PER_PAGE
        current_page = 1

        selected_user = ctx.author.display_name
        embed = self.get_time_stats_embed(selected_user,entries,current_page,page_amount)

        view = discord.ui.View()
        prev_button = discord.ui.Button(label="<", style=discord.ButtonStyle.green)
        next_button = discord.ui.Button(label=">", style=discord.ButtonStyle.blurple)

        async def prev_callback(interaction: discord.Interaction):
            nonlocal current_page
            current_page -= 1
            if current_page < 1:
                current_page = int(len(entries) / self.ENTRIES_PER_PAGE) + 1
            new_embed = self.get_time_stats_embed(selected_user,entries,current_page,page_amount)
            await interaction.response.edit_message(embed=new_embed, view=view)

        async def next_callback(interaction: discord.Interaction):
            nonlocal current_page
            current_page += 1
            if (current_page - 1) * self.ENTRIES_PER_PAGE >= len(entries):
                current_page = 1
            new_embed = self.get_time_stats_embed(selected_user,entries,current_page,page_amount)
            await interaction.response.edit_message(embed=new_embed, view=view)

        prev_button.callback = prev_callback
        next_button.callback = next_callback

        view.add_item(prev_button)
        view.add_item(next_button)

        for user in self.time_database.get_users():
            user_button = discord.ui.Button(label=UserManager.get_display_name(user), style=discord.ButtonStyle.gray)

            async def user_callback(interaction: discord.Interaction, current_user=user):
                nonlocal current_page,entries,page_amount,selected_user
                current_page = 1
                entries = sorted(self.time_database.get_all_time_entries(user=current_user),key=lambda t: t.time_spent,reverse=True)
                page_amount = (len(entries) + self.ENTRIES_PER_PAGE - 1) // self.ENTRIES_PER_PAGE

                selected_user = UserManager.get_display_name(current_user)
                new_embed = self.get_time_stats_embed(selected_user,entries,current_page,page_amount)

                await interaction.response.edit_message(embed=new_embed, view=view)

            user_button.callback = user_callback
            view.add_item(user_button)

        await MessageManager.send_message(ctx, embed=embed,view=view)

    def help(self) -> str:
        return f"- `{ConfigLoader.get_config().command_prefix}timeStats` - Lists playtime's for activities.\n"

    def get_page_entries(self,entries:list[TimeEntry],page:int) -> list[TimeEntry]:
        """
        Returns all entries for a specific page in the time stats list.
        :param entries: All time entries
        :param page: The current page of the list
        :return: A list of time entries for the specified page.
        """
        return entries[self.ENTRIES_PER_PAGE * (page - 1): self.ENTRIES_PER_PAGE * page]

    def get_time_stats_embed(self,user:str,entries:list[TimeEntry],page:int,page_amount) -> discord.Embed:
        """
        Creates and returns the embed for the time stats list.
        :param user: The user for whom the time stats are being displayed.
        :param entries: All time entries for the user.
        :param page: The current page number.
        :param page_amount: The total number of pages.
        :return: Embed object containing the time stats.
        """
        page_entries = self.get_page_entries(entries, page)

        list_txt = ""
        for entry in page_entries:
            hours = TimeUtils.convert_to_hours(entry.time_spent)
            if hours >= 1:
                list_txt += f"- {entry.activity}: {hours} hours\n"
            else:
                list_txt += f"- {entry.activity}: {TimeUtils.convert_to_minutes(entry.time_spent)} minutes\n"

        return MessageManager.get_embed(title=f"{user}'s Time Stats",description=f"{list_txt} Page {page}/{page_amount}")