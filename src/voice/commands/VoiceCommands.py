from discord.ext import commands
from voice.commands.JoinCommand import JoinCommand

class VoiceCommands:
    async def register(self,bot:commands.Bot):
        await bot.add_cog(JoinCommand())

        print("Registered voice commands.")