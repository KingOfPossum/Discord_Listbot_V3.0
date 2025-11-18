from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord import VoiceClient
from discord.ext import commands
from voice.MusicManager import MusicManager
from voice.enums.PauseResponse import PauseResponse
from voice.enums.PlayStatus import PlayStatus

class PauseCommand(Command):
    """
    Command for pausing the current played song.
    """
    @commands.command(name="pause",aliases=["Pause","PAUSE","pauseSong","PauseSong","PAUSESONG","pausesong","pause_song","PAUSE_SONG","Pause_Song"])
    async def execute(self, ctx):
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are not allowed to use this command.")

        response = self.pause(ctx.voice_client)

        match response:
            case PauseResponse.PAUSED:
                await MessageManager.send_message(ctx.channel,f"Paused Song {MusicManager.current_song.title}")
            case PauseResponse.ALREADY_PAUSED:
                await MessageManager.send_error_message(ctx.channel,"Song is already paused")
            case PauseResponse.NO_SONG:
                await MessageManager.send_error_message(ctx.channel,"There is no song to pause")
            case PauseResponse.ERROR:
                await MessageManager.send_error_message(ctx.channel,"Something went wrong")

    def help(self) -> str:
        """
        Returns the help text for the command
        :return: The help text for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}pause` - Pause the current song.\n"

    @staticmethod
    def pause(bot_client:VoiceClient):
        if not MusicManager.current_song:
            return PauseResponse.NO_SONG

        if MusicManager.current_play_status == PlayStatus.PLAYING:
            bot_client.pause()
            MusicManager.current_play_status = PlayStatus.PAUSED
            return PauseResponse.PAUSED

        elif MusicManager.current_play_status == PlayStatus.PAUSED:
            return PauseResponse.ALREADY_PAUSED

        return PauseResponse.ERROR