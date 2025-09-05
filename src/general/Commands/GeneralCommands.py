from general.Commands.ActivateBotRepliesCommand import ActivateBotRepliesCommand
from general.Commands.DeactivateBotRepliesCommand import DeactivateBotRepliesCommand
from general.Commands.RandomizeCommand import RandomizeCommand
from general.Commands.RandomizeNumCommand import RandomizeNumCommand
from discord.ext import commands

from general.Commands.ToggleBotRepliesCommand import ToggleBotRepliesCommand


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
        await bot.add_cog(ActivateBotRepliesCommand())
        await bot.add_cog(DeactivateBotRepliesCommand())
        await bot.add_cog(ToggleBotRepliesCommand())
        print("Registered General cogs.")