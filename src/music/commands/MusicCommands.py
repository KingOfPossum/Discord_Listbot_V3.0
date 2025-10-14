from discord.ext import commands
from music.commands.JoinCommand import JoinCommand
from music.commands.LeaveCommand import LeaveCommand

class MusicCommands:
    """
    This class contains audio/music-related commands for the Discord bot.
    """
    async def register(self,bot:commands.Bot):
        """
        Registers the music commands with the provided bot.
        :param bot: The Discord bot instance to register commands with.
        """
        await bot.add_cog(JoinCommand(bot))
        await bot.add_cog(LeaveCommand(bot))
        print("Registered Music cogs.")