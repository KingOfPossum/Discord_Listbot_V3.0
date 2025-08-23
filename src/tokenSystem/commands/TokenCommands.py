from database.DatabaseCollection import DatabaseCollection
from tokenSystem.commands.AddTokenCommand import AddTokenCommand

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
        print("Registered TokenCommands cogs.")