from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands
from listbot.Commands.AddCommand import AddCommand
from listbot.Commands.CompletedCommand import CompletedCommand
from listbot.Commands.HelpCommand import HelpCommand
from listbot.Commands.RemoveCommand import RemoveCommand
from listbot.Commands.ReplayedCommand import ReplayedCommand
from listbot.Commands.UpdateCommand import UpdateCommand
from listbot.Commands.ViewCommand import ViewCommand

class ListCommands:
    """
    A Discord cog that contains commands related to managing a list of games.
    This cog provides commands to add games.
    """

    def __init__(self,databases: DatabaseCollection):
        """
        Initializes the ListCommands cog.
        """
        self.databases = databases

    async def register(self, bot: commands.Bot):
        """
        Registers the commands in this cog with the provided bot.
        :param bot: The Discord bot instance to register commands with.
        """
        list_database = self.databases.list_database

        await bot.add_cog(AddCommand(list_database))
        await bot.add_cog(UpdateCommand(list_database))
        await bot.add_cog(RemoveCommand(list_database))
        await bot.add_cog(ReplayedCommand(list_database))
        await bot.add_cog(CompletedCommand(list_database))
        await bot.add_cog(ViewCommand(list_database))
        await bot.add_cog(HelpCommand())
        print("Cogs:", list(bot.cogs.keys()))
        print("Commands:", [c.name for c in bot.commands])