from abc import abstractmethod
from discord.ext import commands

class Command(commands.Cog):
    """
    Interface for commands that can be executed in a Discord bot.
    This class defines the structure for commands with a execute method for handling interactions.
    And a help method for providing command usage information.
    """

    @abstractmethod
    async def execute(self,ctx):
        pass

    @abstractmethod
    def help(self) -> str:
        pass