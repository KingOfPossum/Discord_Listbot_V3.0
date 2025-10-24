from discord.ext import commands
from voice.commands.JoinCommand import JoinCommand
from voice.commands.LeaveCommand import LeaveCommand
from voice.commands.PlayCommand import PlayCommand


class VoiceCommands:
    async def register(self,bot:commands.Bot):
        await bot.add_cog(JoinCommand())
        await bot.add_cog(LeaveCommand())
        await bot.add_cog(PlayCommand())

        print("Registered voice commands.")