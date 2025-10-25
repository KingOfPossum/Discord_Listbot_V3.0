from database.ListDatabase import ListDatabase
from discord.ext import commands
from guessingGame.commands.StartGameCommand import StartGameCommand

class GuessingGameCommands:
    """
    Collection of commands concerning the guessing game.
    """
    def __init__(self,list_database:ListDatabase):
        self.list_database = list_database

    async def register(self,bot:commands.Bot):
        """
        Registers all commands concerning the guessing game.
        :param bot: The bot to register the commands with.
        """
        await bot.add_cog(StartGameCommand(self.list_database))
        print("Registered GuessingGame commands cogs.")