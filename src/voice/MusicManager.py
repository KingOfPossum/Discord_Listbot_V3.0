import discord
import os

from common.MessageManager import MessageManager
from voice.PlayStatus import PlayStatus
from voice.VideoEntry import VideoEntry
from voice.VoiceUtils import VoiceUtils

class MusicManager:
    INACTIVE_SECONDS_UNTIL_DISCONNECT = 30
    inactive_time = 0

    current_song: VideoEntry = None
    current_play_status: PlayStatus = PlayStatus.NOTHING
    song_embed: discord.Embed = None
    song_message: discord.Message = None

    def __init__(self,music_folder_path: str):
        self.create_music_folder_if_not_exists(music_folder_path)

    @staticmethod
    def create_music_folder_if_not_exists(music_folder_path: str):
        if not os.path.exists(music_folder_path):
            print(f"Creating music folder at {music_folder_path}")
            os.mkdir(music_folder_path)

    @staticmethod
    def set_current_song(new_song: VideoEntry):
        MusicManager.current_song = new_song

    @staticmethod
    async def send_song_embed(ctx,song: VideoEntry):
        embed = MessageManager.get_embed(title=song.url, description=f"{VoiceUtils.convert_seconds_to_time(song.current_playtime)} - {VoiceUtils.convert_seconds_to_time(song.duration)}")
        embed.set_thumbnail(url=song.thumbnail_url)

        MusicManager.song_embed = embed
        MusicManager.song_message = await MessageManager.send_message(ctx,embed=embed)

    @staticmethod
    async def delete_song_message():
        await MusicManager.song_message.delete()
        MusicManager.song_embed = None
        MusicManager.song_message = None

    @staticmethod
    def reset_inactivity():
        MusicManager.inactive_time = 0