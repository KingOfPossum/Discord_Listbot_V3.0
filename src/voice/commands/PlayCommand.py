from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands
from voice.DownloadManager import DownloadManager
from voice.enums.JoinResponse import JoinResponse
from voice.MusicManager import MusicManager
from voice.commands.JoinCommand import JoinCommand

class PlayCommand(Command):
    """
    Command for playing audio from YouTube in a voice channel.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="play",aliases=["Play","PLAY","playAudio","PlayAudio","PLAYAUDIO","playaudio","playSong","PlaySong","PLAYSONG","playsong"])
    async def execute(self, ctx):
        """
        Executes the PlayCommand.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are not allowed to use this command.")
            return

        response = await JoinCommand.join(ctx.author.voice,ctx.voice_client)

        if not response == JoinResponse.JOINED and not response == JoinResponse.ALREADY_IN_CHANNEL:
            await MessageManager.send_error_message(ctx.channel,"Error while joining channel!")
            return

        url = BotUtils.get_message_content(ctx.message)

        if 'list' in url:
            songs = DownloadManager.search_for_playlist(url)
            if MusicManager.song_queue is None or len(MusicManager.song_queue) == 0:
                await MusicManager.play_song(ctx,songs[0])
                for i in range(1,len(songs)):
                    if not songs[i].title in ["[Deleted video]","[Private video]"]:
                        MusicManager.song_queue.append(songs[i])
            return

        video = DownloadManager.search_for_video(url)

        await MusicManager.play_song(ctx,video)

    def help(self) -> str:
        """
        Returns a help string for the PlayCommand.
        :return: A string describing the PlayCommand.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}play` `url` : Plays audio from a YouTube URL in the voice channel you are connected to\n" +\
                f"- `{ConfigLoader.get_config().command_prefix}play` `videoName` : Searches YouTube for the given video name and plays the first result in the voice channel you are connected to\n"