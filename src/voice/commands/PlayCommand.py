import asyncio
import discord
import os
import re
import yt_dlp

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands

from voice.JoinResponse import JoinResponse
from voice.MusicManager import MusicManager
from voice.PlayStatus import PlayStatus
from voice.VideoEntry import VideoEntry
from voice.commands.JoinCommand import JoinCommand

class PlayCommand(Command):
    """
    Command for playing audio from YouTube in a voice channel.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    youtube_options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{ConfigLoader.get_config().music_folder_path}%(id)s.%(ext)s',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    @commands.command(name="play",aliases=["Play","PLAY","playAudio","PlayAudio","PLAYAUDIO","playaudio","playSong","PlaySong","PLAYSONG","playsong"])
    async def execute(self, ctx):
        """
        Executes the PlayCommand.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are not allowed to use this command.")
            return

        response = await JoinCommand.join(ctx.author.voice,ctx.voice_client)
        print(response.name)

        if not response == JoinResponse.JOINED and not response == JoinResponse.ALREADY_IN_CHANNEL:
            await MessageManager.send_error_message(ctx.channel,"Error while joining channel!")
            return

        url = BotUtils.get_message_content(ctx.message)
        video = self.search_for_video(url)

        print(video)

        # Look if the song has already been downloaded before. If it has just play from the file. Otherwise, download it before playing it.
        if not os.path.exists(ConfigLoader.get_config().music_folder_path + video.video_id  + ".mp3"):
            print(f"Audio not found! Downloading now...")
            self.download_audio_from_url(url)
        source = discord.FFmpegPCMAudio(ConfigLoader.get_config().music_folder_path + video.video_id + ".mp3")

        ctx.voice_client.play(source,after=lambda _: asyncio.run_coroutine_threadsafe(self._after_song(),self.bot.loop))

        MusicManager.set_current_song(video)
        MusicManager.current_play_status = PlayStatus.PLAYING

        await ctx.send(f"**Now Playing** : {video.title}\n{video.thumbnail_url}")

        await MusicManager.send_song_embed(ctx,video)

    def help(self) -> str:
        """
        Returns a help string for the PlayCommand.
        :return: A string describing the PlayCommand.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}play` `url` : Plays audio from a YouTube URL in the voice channel you are connected to\n" +\
                f"- `{ConfigLoader.get_config().command_prefix}play` `videoName` : Searches YouTube for the given video name and plays the first result in the voice channel you are connected to\n"

    @staticmethod
    async def _after_song():
        print("Song ended!")
        MusicManager.set_current_song(None)
        MusicManager.current_play_status = PlayStatus.NOTHING

        await MusicManager.delete_song_message()

    @staticmethod
    def extract_video_id_from_url(url:str) -> str:
        """
        Extracts the YouTube video ID from a YouTube URL.
        :param url: The url of the YouTube video.
        :return: The YouTube video ID of the video.
        """
        regex = re.compile(
            r"^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([^&? ]+)")
        match = regex.search(url)

        if match:
            return match.group(1)
        return None

    @staticmethod
    def search_for_video(query:str) -> VideoEntry:
        """
        Searches YouTube for the given query.
        :param query: The query to search for.
        :return: A VideoEntry object containing relevant information about the video.
        """
        with yt_dlp.YoutubeDL(PlayCommand.youtube_options) as ytdlp:
            info = ytdlp.extract_info(query, download=False)

            if not query.startswith("http"):
                if 'entries' in info:
                    result = info['entries'][0]
                    return VideoEntry.new(result['original_url'], result['title'], result['id'],result['duration'])

            return VideoEntry.new(info['original_url'], info['title'], info['id'],info['duration'])

    @staticmethod
    def download_audio_from_url(url):
        """
        Downloads the audio from a YouTube URL.
        :param url: The URL of the YouTube video.
        """
        with yt_dlp.YoutubeDL(PlayCommand.youtube_options) as ydl:
            ydl.download([url])