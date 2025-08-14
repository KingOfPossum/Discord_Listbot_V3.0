from general.Commands.RandomizeCommand import RandomizeCommand
from general.Commands.RandomizeNumCommand import RandomizeNumCommand
from discord.ext import commands

class GeneralCommands:
    """
    This class contains general commands that are not specific to any particular functionality.
    """

    async def register(self,bot: commands.Bot):
        """
        Registers the general commands with the provided bot.
        :param bot: The Discord bot instance to register commands with.
        """
        await bot.add_cog(RandomizeNumCommand())
        await bot.add_cog(RandomizeCommand())
        print("Registered General cogs.")