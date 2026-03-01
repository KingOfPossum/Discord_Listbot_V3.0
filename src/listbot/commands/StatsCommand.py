import discord

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.MessageManager import MessageManager
from common.TimeUtils import TimeUtils
from common.UserManager import UserManager
from database.DatabaseCollection import DatabaseCollection
from discord import Embed
from discord.ext import commands

class StatsCommand(Command):
    """Command to view statistics about added games in the list and users."""

    @commands.command(name="stats")
    async def execute(self, ctx):
        """Executes the stats command. Viewing statistics about added games in the list and users."""
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel, "You are Not Allowed to use this command")
            return

        year = TimeUtils.get_current_year()
        embed = self.get_main_page_embed(year=year)

        async def back_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=self.get_main_page_embed(year),view=standard_view)

        async def consoles_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=self.get_consoles_stats_embed(year),view=standard_view)

        async def ratings_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=self.get_ratings_stats_embed(year),view=standard_view)

        async def months_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=self.get_months_stats_embed(year),view=standard_view)

        async def users_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=embed,view=user_stats_view)

        standard_view = discord.ui.View()

        back_button = discord.ui.Button(label="Back",style=discord.ButtonStyle.red)
        back_button.callback = back_callback

        consoles_button = discord.ui.Button(label="Consoles",style=discord.ButtonStyle.green)
        consoles_button.callback = consoles_callback

        ratings_button = discord.ui.Button(label="Ratings",style=discord.ButtonStyle.green)
        ratings_button.callback = ratings_callback

        months_button = discord.ui.Button(label="Months",style=discord.ButtonStyle.green)
        months_button.callback = months_callback

        user_stats_button = discord.ui.Button(label="Users",style=discord.ButtonStyle.blurple)
        user_stats_button.callback = users_callback

        standard_view.add_item(back_button)
        standard_view.add_item(consoles_button)
        standard_view.add_item(ratings_button)
        standard_view.add_item(months_button)
        standard_view.add_item(user_stats_button)

        user_stats_view = discord.ui.View()

        user_stats_view.add_item(back_button)
        for user in UserManager.accepted_users:
            user_entry = UserManager.get_user_entry(user_name=user.name)

            if DatabaseCollection.list_database.does_user_have_entries(user_entry.user_id):
                user_button = discord.ui.Button(label=user.display_name,style=discord.ButtonStyle.gray)

                async def user_callback(interaction: discord.Interaction,current_user=user):
                    await interaction.response.edit_message(embed=self.get_user_stats_embed(current_user.id,year=year), view=user_stats_view)

                user_button.callback = user_callback
                user_stats_view.add_item(user_button)

        year_buttons = {}
        years = DatabaseCollection.list_database.get_years()

        # Insert None at the beginning of the list to represent the total stats
        years.insert(0,None)

        # Create a button for each year and add it to the standard view. When a button is clicked, the main page embed is updated to show the stats for the selected year. And the button is disabled to indicate that it is the currently selected year.
        for _year in years:
            year_button = discord.ui.Button(label=_year if _year is not None else "Total",style=discord.ButtonStyle.gray)

            year_buttons[_year] = year_button
            if _year == str(TimeUtils.get_current_year()):
                year_buttons[_year].disabled = True

            async def year_callback(interaction: discord.Interaction,current_year=_year):
                nonlocal year
                year = current_year

                for yb in year_buttons.values():
                    yb.disabled = False
                year_buttons[current_year].disabled = True

                await interaction.response.edit_message(embed=self.get_main_page_embed(year), view=standard_view)

            year_button.callback = year_callback
            standard_view.add_item(year_button)

        await ctx.send(embed=embed,view=standard_view)

    def help(self) -> str:
        """Returns a string that describes the command and how to use it."""
        return f"- `{ConfigLoader.get_config().command_prefix}stats` - View statistics.\n"

    def get_main_page_embed(self, year:int = None) -> Embed:
        """
        Creates the main stats embed which shows up to three entries for each stat.
        :param year: The year for which the stats are shown.
        :return: the main stats embed.
        """
        user_game_counts = DatabaseCollection.list_database.get_user_game_counts(year=year,limit=3)
        highest_rated_games = DatabaseCollection.list_database.get_highest_rated_games(year=year,limit=3)
        worst_rated_games = DatabaseCollection.list_database.get_worst_rated_games(year=year,limit=3)
        months_counts = DatabaseCollection.list_database.get_months_counts(year=year)
        console_counts = DatabaseCollection.list_database.get_console_counts(year=year,limit=3)
        genre_counts = DatabaseCollection.list_database.get_genre_counts(year=year,limit=3)

        embed = discord.Embed(title=f"Stats ({year if year else "Total"})", color=0x00ff00)
        embed.add_field(name="", value=f"**Games Played:**\n{self.convert_to_string(user_game_counts)}\n"
                                       f"**Highest Rated Games:**\n{self.convert_to_string(highest_rated_games)}\n"
                                       f"**Worst Rated Games:**\n{self.convert_to_string(worst_rated_games)}\n")
        embed.add_field(name="", value=f"**Most Used Console:**\n{self.convert_to_string(console_counts)}\n"
                                       f"**Most Active Month:**\n{self.convert_to_string(months_counts)}\n"
                                       f"**Most Played Genre:**\n{self.convert_to_string(genre_counts)}\n")
        return embed

    def get_user_stats_embed(self,user_id:int,year:int = None) -> Embed:
        """
        Creates the user stats embed which shows up to three entries for each stat.
        :param user_id: The ID of the user for which the stats are shown.
        :param year: The year for which the stats are shown.
        :return: The user stats embed.
        """
        highest_rated_games = DatabaseCollection.list_database.get_highest_rated_games(user_id=user_id,year=year,limit=3)
        worst_rated_games = DatabaseCollection.list_database.get_worst_rated_games(user_id=user_id,year=year,limit=3)
        console_counts = DatabaseCollection.list_database.get_console_counts(user_id=user_id,year=year,limit=3)
        months_counts = DatabaseCollection.list_database.get_months_counts(user_id=user_id,year=year,limit=3)
        genre_counts = DatabaseCollection.list_database.get_genre_counts(user_id=user_id,year=year,limit=3)

        embed = discord.Embed(title=f"{UserManager.get_user_entry(user_id=user_id).display_name}'s Stats ({year if year else "Total"})",color=0x00ff00)
        embed.add_field(name="",value=f"**Highest Rated Games:**\n{self.convert_to_string(highest_rated_games)}\n"
                                      f"**Worst Rated Games:**\n{self.convert_to_string(worst_rated_games)}\n")
        embed.add_field(name="",value=f"**Most Used Console:**\n{self.convert_to_string(console_counts)}\n"
                                      f"**Most Active Month:**\n{self.convert_to_string(months_counts)}\n"
                                      f"**Most Played Genre:**\n{self.convert_to_string(genre_counts)}")
        return embed

    def get_consoles_stats_embed(self,year:int) -> Embed:
        """
        Creates the consoles stats embed which shows the top 10 most used consoles.
        :param year: The year for which the stats are shown.
        :return: The consoles stats embed.
        """
        embed = discord.Embed(title=f"Most Used Consoles ({year if year else "Total"})", color=0x00ff00)
        console_counts = DatabaseCollection.list_database.get_console_counts(year=year,limit=10)

        consoles_txt = "\n".join([f"- {entry[0]} : {entry[1]}" for entry in console_counts])
        embed.add_field(name="", value=consoles_txt)

        return embed

    def get_ratings_stats_embed(self,year:int) -> Embed:
        """
        Creates the ratings stats embed which shows the top 10 highest rated games.
        :param year: The year for which the stats are shown.
        :return: The ratings stats embed.
        """
        embed = discord.Embed(title=f"Highest Rated Games ({year if year else "Total"})", color=0x00ff00)
        highest_rated_games = DatabaseCollection.list_database.get_highest_rated_games(year=year,limit=10)

        ratings_txt = "\n".join([f"- {entry[0]} : {entry[1]}" for entry in highest_rated_games])
        embed.add_field(name="", value=ratings_txt)

        return embed

    def get_months_stats_embed(self,year:int) -> Embed:
        """
        Creates the months stats embed which shows the top 10 most active months.
        :param year: The year for which the stats are shown.
        :return: The months stats embed.
        """
        embed = discord.Embed(title=f"Most Active Months ({year if year else "Total"})", color=0x00ff00)
        months_counts = DatabaseCollection.list_database.get_months_counts(year=year,limit=10)

        months_txt = "\n".join([f"- {entry[0]} : {entry[1]}" for entry in months_counts])
        embed.add_field(name="", value=months_txt)

        return embed

    def convert_to_string(self,entries: list[tuple[str,int]]) -> list[str]:
        """
        Converts a list of tuples to a list of formatted strings.
        :param entries: list of tuples containing a name and a count
        :return: list of formatted strings
        """
        txt = ""
        for i in range(len(entries)):
            # Only show top 3 entries otherwise it will throw list index out of range exception because of the emojis
            if i > 2:
                break
            txt += f"{Emojis.RANKINGS[i]} {entries[i][0]} : { entries[i][1]}\n"
        return txt