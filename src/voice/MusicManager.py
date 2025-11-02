import discord
import os

from common.Emojis import Emojis
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
    song_view: discord.ui.View = None
    song_embed_buttons: dict = {}
    song_message: discord.Message = None
    bot_voice_client: discord.VoiceClient = None

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
        MusicManager.bot_voice_client = ctx.voice_client

        embed = MessageManager.get_embed(title=f"", description=f"[{song.title}]({song.url})\n{VoiceUtils.convert_seconds_to_time(song.current_playtime)} - {VoiceUtils.convert_seconds_to_time(song.duration)}")
        embed.set_thumbnail(url=song.thumbnail_url)

        view = discord.ui.View()

        pause_button = discord.ui.Button(label=Emojis.PAUSE,style=discord.ButtonStyle.primary)
        pause_button.callback = MusicManager.pause_callback

        stop_button = discord.ui.Button(label=Emojis.STOP,style=discord.ButtonStyle.primary)
        stop_button.callback = MusicManager.stop_callback

        shuffle_button = discord.ui.Button(label=Emojis.SHUFFLE,style=discord.ButtonStyle.red)
        shuffle_button.callback = MusicManager.shuffle_callback

        loop_button = discord.ui.Button(label=Emojis.LOOP,style=discord.ButtonStyle.red)
        loop_button.callback = MusicManager.loop_callback

        view.add_item(shuffle_button)
        view.add_item(loop_button)
        view.add_item(stop_button)
        view.add_item(pause_button)

        MusicManager.song_embed_buttons["shuffle"] = shuffle_button
        MusicManager.song_embed_buttons["loop"] = loop_button
        MusicManager.song_embed_buttons["stop"] = stop_button
        MusicManager.song_embed_buttons["pause/resume"] = pause_button

        MusicManager.song_embed = embed
        MusicManager.song_view = view
        MusicManager.song_message = await MessageManager.send_message(ctx,embed=embed,view=view)

    @staticmethod
    async def delete_song_message():
        if MusicManager.song_message:
            await MusicManager.song_message.delete()
        MusicManager.song_embed = None
        MusicManager.song_message = None
        MusicManager.song_view = None
        MusicManager.song_embed_buttons = {}

    @staticmethod
    def reset_inactivity():
        MusicManager.inactive_time = 0

    async def pause_callback(interaction:discord.Interaction):
        from voice.commands.PauseCommand import PauseCommand
        PauseCommand.pause(MusicManager.bot_voice_client)

        resume_button = discord.ui.Button(label=Emojis.RESUME,style=discord.ButtonStyle.primary)
        resume_button.callback = MusicManager.resume_callback

        MusicManager.song_view.remove_item(MusicManager.song_embed_buttons["pause/resume"])
        MusicManager.song_embed_buttons["pause/resume"] = resume_button
        MusicManager.song_view.add_item(MusicManager.song_embed_buttons["pause/resume"])

        await interaction.response.edit_message(embed=MusicManager.song_embed,view=MusicManager.song_view)

    async def resume_callback(interaction:discord.Interaction):
        from voice.commands.ResumeCommand import ResumeCommand
        ResumeCommand.resume(MusicManager.bot_voice_client)

        pause_button = discord.ui.Button(label=Emojis.PAUSE,style=discord.ButtonStyle.primary)
        pause_button.callback = MusicManager.pause_callback

        MusicManager.song_view.remove_item(MusicManager.song_embed_buttons["pause/resume"])
        MusicManager.song_embed_buttons["pause/resume"] = pause_button
        MusicManager.song_view.add_item(MusicManager.song_embed_buttons["pause/resume"])

        await interaction.response.edit_message(embed=MusicManager.song_embed,view=MusicManager.song_view)

    async def stop_callback(interaction:discord.Interaction):
        from voice.commands.StopCommand import StopCommand
        StopCommand.stop(MusicManager.bot_voice_client)
        await interaction.response.defer()

    async def shuffle_callback(interaction:discord.Interaction):
        pass

    async def loop_callback(interaction:discord.Interaction):
        pass