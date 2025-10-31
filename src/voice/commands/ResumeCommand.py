from discord import VoiceClient

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

from voice.MusicManager import MusicManager
from voice.PlayStatus import PlayStatus
from voice.ResumeResponse import ResumeResponse


class ResumeCommand(Command):
    @commands.command(name="resume")
    async def execute(self, ctx):
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are not allowed to use this command")

        response = self.resume(ctx.voice_client)

        match response:
            case ResumeResponse.RESUMED:
                await MessageManager.send_message(ctx.channel,f"Resuming song {MusicManager.current_song.title}!")
            case ResumeResponse.ALREADY_PLAYING:
                await MessageManager.send_error_message(ctx.channel,"Already playing song!")
            case ResumeResponse.NO_SONG:
                await MessageManager.send_error_message(ctx.channel,"There is no song playing right now!")
            case ResumeResponse.ERROR:
                await MessageManager.send_error_message(ctx.channel,"Something went wrong!")

    def help(self) -> str:
        """
        Returns the help message for this command
        :return: The help message for this command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}resume` : Resumes the current song"

    @staticmethod
    def resume(bot_voice: VoiceClient) -> ResumeResponse:
        """
        Resumes the current song
        :return: Resume response
        """
        if not MusicManager.current_song:
            return ResumeResponse.NO_SONG

        if MusicManager.current_play_status == PlayStatus.PLAYING:
            return ResumeResponse.ALREADY_PLAYING

        if MusicManager.current_play_status == PlayStatus.PAUSED:
            bot_voice.resume()
            MusicManager.current_play_status = PlayStatus.PLAYING
            return ResumeResponse.RESUMED

        return ResumeResponse.ERROR