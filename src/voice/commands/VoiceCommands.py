from discord.ext import commands
from voice.commands.JoinCommand import JoinCommand
from voice.commands.LeaveCommand import LeaveCommand
from voice.commands.PauseCommand import PauseCommand
from voice.commands.PlayCommand import PlayCommand
from voice.commands.ResumeCommand import ResumeCommand
from voice.commands.StopCommand import StopCommand

class VoiceCommands:
    async def register(self,bot:commands.Bot):
        await bot.add_cog(JoinCommand())
        await bot.add_cog(LeaveCommand())
        await bot.add_cog(PlayCommand(bot))
        await bot.add_cog(PauseCommand())
        await bot.add_cog(ResumeCommand())
        await bot.add_cog(StopCommand())

        print("Registered voice commands.")