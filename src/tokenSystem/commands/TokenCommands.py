from database.DatabaseCollection import DatabaseCollection
from tokenSystem.commands.AddTokenCommand import AddTokenCommand
from tokenSystem.commands.RemoveCoinCommand import RemoveCoinCommand
from tokenSystem.commands.SetNeededCoinsCommand import SetNeededCoinsCommand
from tokenSystem.commands.ViewTokensCommand import ViewTokensCommand

class TokenCommands:
    """
    A Discord cog that contains commands related to managing the token system.
    """

    async def register(self,bot):
        """
        Registers the commands in this cog with the provided bot.
        :param bot: The bot to register the commands with.
        """
        await bot.add_cog(AddTokenCommand())
        await bot.add_cog(RemoveCoinCommand())
        await bot.add_cog(SetNeededCoinsCommand())
        await bot.add_cog(ViewTokensCommand())
        print("Registered TokenCommands cogs.")