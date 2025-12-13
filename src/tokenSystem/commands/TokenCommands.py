from database_.DatabaseCollection import DatabaseCollection
from tokenSystem.commands.AddTokenCommand import AddTokenCommand
from tokenSystem.commands.RemoveCoinCommand import RemoveCoinCommand
from tokenSystem.commands.SetNeededCoinsCommand import SetNeededCoinsCommand
from tokenSystem.commands.ViewTokensCommand import ViewTokensCommand

class TokenCommands:
    """
    A Discord cog that contains commands related to managing the token system.
    """
    def __init__(self,databases: DatabaseCollection):
        self.databases = databases

    async def register(self,bot):
        """
        Registers the commands in this cog with the provided bot.
        :param bot: The bot to register the commands with.
        """
        database = self.databases.tokens_database

        await bot.add_cog(AddTokenCommand(database))
        await bot.add_cog(RemoveCoinCommand(database))
        await bot.add_cog(SetNeededCoinsCommand(database))
        await bot.add_cog(ViewTokensCommand(database))
        print("Registered TokenCommands cogs.")