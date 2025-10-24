from discord.ext import commands
from voice.commands.JoinCommand import JoinCommand
from voice.commands.LeaveCommand import LeaveCommand

class VoiceCommands:
    async def register(self,bot:commands.Bot):
        await bot.add_cog(JoinCommand())
        await bot.add_cog(LeaveCommand())

        print("Registered voice commands.")