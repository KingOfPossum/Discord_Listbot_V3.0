import discord
import os
import random
import threading

from common.Emojis import Emojis
from common.MessageManager import MessageManager
from discord.ext import commands
from voice.enums.PlayResponse import PlayResponse
from voice.enums.PlayStatus import PlayStatus
from voice.VideoEntry import VideoEntry
from voice.VoiceUtils import VoiceUtils

class MusicManager:
    INACTIVE_SECONDS_UNTIL_DISCONNECT = 300 # 5 Minutes
    inactive_time = 0

    current_song: VideoEntry = None
    song_queue: list[VideoEntry] = []
    current_song_index: int = 0
    next_song_index: int = 0
    next_song_entry: VideoEntry = None
    current_play_status: PlayStatus = PlayStatus.NOTHING

    current_ctx:commands.Context = None

    song_embed: discord.Embed = None
    song_view: discord.ui.View = None
    song_embed_buttons: dict = {}
    song_message: discord.Message = None
    bot_voice_client: discord.VoiceClient = None

    shuffle: bool = False
    looping: bool = False

    def __init__(self,music_folder_path: str):
        self.create_music_folder_if_not_exists(music_folder_path)

    @staticmethod
    def create_music_folder_if_not_exists(music_folder_path: str):
        if not os.path.exists(music_folder_path):
            print(f"Creating music folder at {music_folder_path}")
            os.mkdir(music_folder_path)

    @staticmethod
    async def send_song_embed(ctx,song: VideoEntry):
        MusicManager.bot_voice_client = ctx.voice_client

        embed = MessageManager.get_embed(title=f"", description=f"[{song.title}]({song.url})\n{VoiceUtils.convert_seconds_to_time(song.current_playtime)} - {VoiceUtils.convert_seconds_to_time(song.duration)}")
        embed.set_thumbnail(url=song.thumbnail_url)
        embed.add_field(name=f"Songs in Queue: {len(MusicManager.song_queue)}", value="", inline=False)

        view = discord.ui.View()
        view.timeout = None

        pause_button = discord.ui.Button(label=Emojis.PAUSE,style=discord.ButtonStyle.primary)
        pause_button.callback = MusicManager.pause_callback

        stop_button = discord.ui.Button(label=Emojis.STOP,style=discord.ButtonStyle.primary)
        stop_button.callback = MusicManager.stop_callback

        skip_button = discord.ui.Button(label=Emojis.SKIP,style=discord.ButtonStyle.primary)
        skip_button.callback = MusicManager.skip_callback

        shuffle_button = discord.ui.Button(label=Emojis.SHUFFLE,style=discord.ButtonStyle.red)
        shuffle_button.callback = MusicManager.shuffle_callback

        loop_button = discord.ui.Button(label=Emojis.LOOP,style=discord.ButtonStyle.red)
        loop_button.callback = MusicManager.loop_callback

        view.add_item(shuffle_button)
        view.add_item(loop_button)
        view.add_item(stop_button)
        view.add_item(skip_button)
        view.add_item(pause_button)

        MusicManager.song_embed_buttons["shuffle"] = shuffle_button
        MusicManager.song_embed_buttons["loop"] = loop_button
        MusicManager.song_embed_buttons["stop"] = stop_button
        MusicManager.song_embed_buttons["skip"] = skip_button
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

    @staticmethod
    async def next_song():
        print([song.title for song in MusicManager.song_queue])

        if not MusicManager.song_queue or len(MusicManager.song_queue) == 0:
            await MusicManager.delete_song_message()
            return

        if len(MusicManager.song_queue) > 0:
            MusicManager.song_queue.pop(MusicManager.current_song_index)
            if MusicManager.looping:
                if MusicManager.current_song:
                    MusicManager.song_queue.append(MusicManager.current_song)

            if MusicManager.shuffle:
                if not MusicManager.next_song_entry:
                    MusicManager.current_song_index = random.randint(0,len(MusicManager.song_queue)-1)
                else:
                    MusicManager.current_song_index = MusicManager.song_queue.index(MusicManager.next_song_entry)
                MusicManager.next_song_index = random.randint(0,len(MusicManager.song_queue)-1)
            else:
                MusicManager.next_song_index = 1
                MusicManager.current_song_index = 0

            next_song = MusicManager.song_queue[MusicManager.current_song_index]
            MusicManager.next_song_entry = MusicManager.song_queue[MusicManager.next_song_index]

            MusicManager.current_song = None
            MusicManager.current_play_status = PlayStatus.NOTHING

            if MusicManager.current_ctx:
                print("Playing next song:",next_song.title)
                await MusicManager.play_song(MusicManager.current_ctx,next_song,True)

                downloader = threading.Thread(target=MusicManager.next_song_entry.download,daemon=True)
                downloader.start()
                print(f"Started downloading next song in background (Thread: {downloader.ident}) : {MusicManager.next_song_entry.title}")

    @staticmethod
    async def play_song(ctx,song: VideoEntry,force: bool = False):
        MusicManager.current_ctx = ctx

        if not force:
            if MusicManager.current_song:
                MusicManager.song_queue.append(song)
                return
            MusicManager.song_queue.append(song)

        MusicManager.current_song = song
        response = await MusicManager.current_song.play(ctx.voice_client)

        match response:
            case PlayResponse.SUCCESS:
                MusicManager.current_play_status = PlayStatus.PLAYING
                if not MusicManager.song_embed:
                    await MusicManager.send_song_embed(ctx,song)
            case PlayResponse.ANOTHER_SONG_IS_PLAYING:
                await MessageManager.send_error_message(ctx.channel,"Another song is already playing!")
            case PlayResponse.ERROR:
                await MessageManager.send_error_message(ctx.channel,"Error while trying to play the song!")

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
        await StopCommand.stop(MusicManager.bot_voice_client)
        await interaction.response.defer()

    async def skip_callback(interaction:discord.Interaction):
        if len(MusicManager.song_queue) <= 1 and not MusicManager.looping:
            await MusicManager.stop_callback(interaction)
            return

        MusicManager.bot_voice_client.stop()
        await interaction.response.defer()

    async def shuffle_callback(interaction:discord.Interaction):
        MusicManager.shuffle = not MusicManager.shuffle
        MusicManager.song_embed_buttons["shuffle"].style = discord.ButtonStyle.green if MusicManager.shuffle else discord.ButtonStyle.red
        await interaction.response.edit_message(embed=MusicManager.song_embed,view=MusicManager.song_view)

    async def loop_callback(interaction:discord.Interaction):
        MusicManager.looping = not MusicManager.looping
        MusicManager.song_embed_buttons["loop"].style = discord.ButtonStyle.green if MusicManager.looping else discord.ButtonStyle.red
        await interaction.response.edit_message(embed=MusicManager.song_embed, view=MusicManager.song_view)