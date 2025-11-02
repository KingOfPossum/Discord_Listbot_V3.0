from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.UserManager import UserManager
from common.MessageManager import MessageManager
from discord import VoiceClient
from discord.ext import commands
from voice.MusicManager import MusicManager
from voice.PlayStatus import PlayStatus
from voice.StopResponse import StopResponse

class StopCommand(Command):
    """
    Command for stopping the current played song.
    """
    @commands.command(name="stop",aliases=["Stop","STOP","stopSong","STOPSONG","stopsong","stop_song","Stop_Song","STOP_SONG","stop_Song"])
    async def execute(self, ctx):
        if not UserManager.is_user_accepted(ctx.author):
            await MessageManager.send_error_message(ctx.channel,"You are not allowed to use this command.")
            return

        response = self.stop(ctx.voice_client)

        match response:
            case StopResponse.STOPPED_SONG:
                await MessageManager.send_message(ctx.channel,f"Stopped song {MusicManager.current_song.title}")
            case StopResponse.NO_SONG:
                await MessageManager.send_error_message(ctx.channel,"There is no song playing!")
            case StopResponse.ERROR:
                await MessageManager.send_error_message(ctx.channel,"Something went wrong!")

    def help(self) -> str:
        """
        Returns the help string for this command.
        :return: The help string.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}stop` : Stops the current played Song\n"

    @staticmethod
    def stop(bot_client:VoiceClient):
        """
        Stops the current played song.
        :param bot_client: The bots voice client.
        :return: A StopResponse object representing the result of the stop command.
        """
        if not MusicManager.current_song:
            return StopResponse.NO_SONG

        try:
            bot_client.stop()
            MusicManager.current_play_status = PlayStatus.NOTHING
            MusicManager.current_song = None
            MusicManager.delete_song_message()
            return StopResponse.STOPPED_SONG
        except Exception:
            return StopResponse.ERROR