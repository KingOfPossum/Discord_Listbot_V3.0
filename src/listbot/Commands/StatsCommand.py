import discord
from discord import Embed

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.GameEntry import GameEntry
from common.TimeUtils import TimeUtils
from database.ListDatabase import ListDatabase
from discord.ext import commands

class StatsCommand(Command):
    """Command to view statistics about added games in the list and users."""
    def __init__(self, list_database: ListDatabase):
        self.list_database = list_database

    @commands.command(name="stats")
    async def execute(self, ctx):
        """Executes the stats command. Viewing statistics about added games in the list and users."""
        game_entries, highest_rated_games, worst_rated_games, user_game_counts, months_counts, console_counts = self.get_stats(TimeUtils.get_current_year())

        embed = self.get_main_page_embed(user_game_counts, highest_rated_games, worst_rated_games, months_counts, console_counts)

        async def back_callback(interaction: discord.Interaction):
            new_embed = self.get_main_page_embed(user_game_counts, highest_rated_games, worst_rated_games, months_counts, console_counts)
            await interaction.response.edit_message(embed=new_embed,view=view)

        async def consoles_callback(interaction: discord.Interaction):
            new_embed = self.get_consoles_stats_embed(console_counts)
            await interaction.response.edit_message(embed=new_embed,view=view)

        async def ratings_callback(interaction: discord.Interaction):
            new_embed = self.get_ratings_stats_embed(game_entries)
            await interaction.response.edit_message(embed=new_embed,view=view)

        async def months_callback(interaction: discord.Interaction):
            new_embed = self.get_months_stats_embed(months_counts)
            await interaction.response.edit_message(embed=new_embed,view=view)

        view = discord.ui.View()

        back_button = discord.ui.Button(label="Back",style=discord.ButtonStyle.red)
        back_button.callback = back_callback

        consoles_button = discord.ui.Button(label="Consoles",style=discord.ButtonStyle.green)
        consoles_button.callback = consoles_callback

        ratings_button = discord.ui.Button(label="Ratings",style=discord.ButtonStyle.green)
        ratings_button.callback = ratings_callback

        months_button = discord.ui.Button(label="Months",style=discord.ButtonStyle.green)
        months_button.callback = months_callback

        view.add_item(back_button)
        view.add_item(consoles_button)
        view.add_item(ratings_button)
        view.add_item(months_button)

        year_buttons = {}
        years = self.list_database.get_years()
        years.insert(0,None)
        for year in years:
            year_button = discord.ui.Button(label=year if year is not None else "Total",style=discord.ButtonStyle.gray)

            year_buttons[year] = year_button
            if year == str(TimeUtils.get_current_year()):
                year_buttons[year].disabled = True

            async def year_callback(interaction: discord.Interaction,current_year=year):
                nonlocal game_entries, highest_rated_games, worst_rated_games, user_game_counts, months_counts, console_counts
                game_entries, highest_rated_games, worst_rated_games, user_game_counts, months_counts, console_counts = self.get_stats(year=current_year)

                new_embed = self.get_main_page_embed(user_game_counts, highest_rated_games, worst_rated_games, months_counts, console_counts)

                for yb in year_buttons.values():
                    yb.disabled = False
                year_buttons[current_year].disabled = True

                await interaction.response.edit_message(embed=new_embed, view=view)

            year_button.callback = year_callback
            view.add_item(year_button)

        await ctx.send(embed=embed,view=view)

    def help(self) -> str:
        """Returns a string that describes the command and how to use it."""
        return f"- `{ConfigLoader.get_config().command_prefix}stats` - View statistics.\n"

    def get_stats(self,year=None) -> tuple:
        """
        Gets statistics about added games in the list.
        Will return the following statistics:
        - Highest Rated Games
        - Worst Rated Games
        - Most Active Users
        - Most Active Months
        - Most Used Consoles
        :param year: The year to filter the statistics. If None, consider all years.
        :return: A tuple containing lists of statistics.
        """
        game_entries = self.list_database.get_all_game_entries(year=year)
        print(game_entries)

        highest_rated_games = [(entry.name, entry.rating) for entry in
                               sorted(game_entries, key=lambda x: x.rating, reverse=True)[:3]]
        worst_rated_games = [(entry.name, entry.rating) for entry in sorted(game_entries, key=lambda x: x.rating)[:3]]
        user_game_counts = self.get_user_game_counts(game_entries)[:3]
        months_counts = self.get_months_counts(game_entries)
        console_counts = self.get_console_counts(game_entries)[:3]

        return game_entries,highest_rated_games, worst_rated_games, user_game_counts, months_counts, console_counts

    def get_main_page_embed(self, user_game_counts, highest_rated_games, worst_rated_games, months_counts, console_counts) -> Embed:
        """
        Creates the main stats embed which shows up to three entries for each stat.
        :param user_game_counts: The amount of games added per user.
        :param highest_rated_games: The highest rated games.
        :param worst_rated_games: The worst rated games.
        :param months_counts: The amount of games added per month.
        :param console_counts: The amount of games added per console.
        :return: the main stats embed.
        """
        embed = discord.Embed(title="Stats", color=0x00ff00)
        embed.add_field(name="", value=f"**Games Played:**\n{self.convert_to_string(user_game_counts)}\n"
                                       f"**Highest Rated Games:**\n{self.convert_to_string(highest_rated_games)}\n"
                                       f"**Worst Rated Games:**\n{self.convert_to_string(worst_rated_games)}\n")
        embed.add_field(name="", value=f"**Most Used Console:**\n{self.convert_to_string(console_counts)}\n"
                                       f"**Most Active Month:**\n{self.convert_to_string(months_counts)}\n")
        return embed

    def get_consoles_stats_embed(self,console_counts) -> Embed:
        """
        Creates the consoles stats embed which shows the top 10 most used consoles.
        :param console_counts: The amount of games added per console.
        :return: The consoles stats embed.
        """
        embed = discord.Embed(title="Most Used Consoles", color=0x00ff00)
        consoles_txt = "\n".join([f"- {entry[0]} : {entry[1]}" for entry in console_counts[:10]])
        embed.add_field(name="", value=consoles_txt)

        return embed

    def get_ratings_stats_embed(self,game_entries) -> Embed:
        """
        Creates the ratings stats embed which shows the top 10 highest rated games.
        :return: The ratings stats embed.
        """
        embed = discord.Embed(title="Highest Rated Games", color=0x00ff00)
        ratings_txt = "\n".join([f"- {entry[0]} : {entry[1]}" for entry in [(entry.name, entry.rating) for entry in sorted(game_entries, key=lambda x: x.rating,reverse=True)[:10]]])
        embed.add_field(name="", value=ratings_txt)

        return embed

    def get_months_stats_embed(self,months_counts) -> Embed:
        """
        Creates the months stats embed which shows the top 10 most active months.
        :param months_counts: The amount of games added per month.
        :return: The months stats embed.
        """
        embed = discord.Embed(title="Most Active Months", color=0x00ff00)
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

    def get_user_game_counts(self,game_entries: list[GameEntry]) -> list[tuple[str, int]]:
        """
        Returns the amount of games added per user in a list of tuples
        :param game_entries: list of all game entries
        :return list of tuples containing usernames and amount of games added
        """
        game_counts = {}

        for entry in game_entries:
            try:
                game_counts[entry.user] += 1
            except KeyError:
                game_counts[entry.user] = 1

        return [(user, count) for user,count in sorted(game_counts.items(), key=lambda item: item[1], reverse=True)]

    def get_months_counts(self,game_entries: list[GameEntry]) -> list[tuple[str,int]]:
        """
        Returns the amount of games added per month  in a list of tuples
        :param game_entries: list of all game entries
        :return: list of tuples containing month names and amount of games added
        """
        month_counts = {}

        for entry in game_entries:
            month = entry.date.split("-")[1]
            MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            month = MONTHS[int(month)-1]

            try:
                month_counts[month] += 1
            except KeyError:
                month_counts[month] = 1

        return [(month, count) for month,count in sorted(month_counts.items(), key=lambda item: item[1], reverse=True)]

    def get_console_counts(self,game_entries: list[GameEntry]) -> list[tuple[str,int]]:
        """
        Returns the amount of games added per console in a list of tuples
        :param game_entries: list of all game entries
        :return: list of tuples containing console names and amount of games added
        """
        console_counts = {}

        for entry in game_entries:
            try:
                console_counts[entry.console] += 1
            except KeyError:
                console_counts[entry.console] = 1

        return [(console, count) for console,count in sorted(console_counts.items(), key=lambda item: item[1], reverse=True)]