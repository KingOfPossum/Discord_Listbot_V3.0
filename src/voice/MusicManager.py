import discord
import os
import random

from common.Emojis import Emojis
from common.MessageManager import MessageManager
from discord.ext import commands
from voice.enums.PlayResponse import PlayResponse
from voice.enums.PlayStatus import PlayStatus
from voice.VideoEntry import VideoEntry
from voice.VoiceUtils import VoiceUtils

class MusicManager:
    """
    Class for managing the actual audio playing logic
    Handles the song queue and which song to play or download next
    """
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
        """
        Creates the music folder if it doesn't exist already.
        Used to store all cached audio files
        """
        if not os.path.exists(music_folder_path):
            print(f"Creating music folder at {music_folder_path}")
            os.mkdir(music_folder_path)

    @staticmethod
    async def send_song_embed(ctx,song: VideoEntry):
        """
        Send the song embed containing information about the current song with its url,
        but also about the next played song if there is one and how many songs are in the queue.
        Also has buttons for pausing,skipping,stopping,shuffle,looping.
        :param ctx: The context in which the message should be send
        :param song: The song for which to send the message for
        """
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

        skip_button = discord.ui.Button(label=Emojis.SKIP,style=discord.ButtonStyle.primary,disabled=True)
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
        """
        Delete the song message and reset embed,message,view,buttons variables
        """
        if MusicManager.song_message:
            await MusicManager.song_message.delete()
        MusicManager.song_embed = None
        MusicManager.song_message = None
        MusicManager.song_view = None
        MusicManager.song_embed_buttons = {}

    @staticmethod
    def reset_inactivity():
        """
        Reset the current time that the bot was inactive
        """
        MusicManager.inactive_time = 0

    @staticmethod
    def set_next_song():
        """
        Sets the next song to be played based on the current shuffle setting.
        """
        if MusicManager.shuffle:
            MusicManager.next_song_index = random.randint(0,len(MusicManager.song_queue)-1)
        else:
            MusicManager.next_song_index = 1
        MusicManager.next_song_entry = MusicManager.song_queue[MusicManager.next_song_index]

    @staticmethod
    async def next_song():
        """
        Plays the next song in the song_queue.
        If the song_queue is empty then bot is finished playing and the song message will be deleted.
        If looping: We append the last played song to the end of the queue
        If shuffle: The next song is a random one. Otherwise the next song is simply the next in the queue
        After starting the next song, will try to preload the next song to improve performance
        """
        print("FINISHED ASDIOJJJJJJJJJJJJJJJJJJ")
        if not MusicManager.song_queue or len(MusicManager.song_queue) <= 1:
            from voice.commands.StopCommand import StopCommand
            await StopCommand.stop(MusicManager.bot_voice_client)
            return

        MusicManager.song_queue.pop(MusicManager.current_song_index)
        if len(MusicManager.song_queue) > 0:
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

                await MusicManager.download_next_song()

    @staticmethod
    async def download_next_song():
        """
        Tries to preload the next song.
        If an error occurrs then we will remove the song from the queue and try to preload the next song.
        """
        if not MusicManager.next_song_entry:
            return

        result = await MusicManager.next_song_entry.download()

        if not result:
            print(f"Error while downloading. Probably due to unavailable video. Skipping to next song.")
            MusicManager.song_queue.remove(MusicManager.next_song_entry)
            MusicManager.set_next_song()

            await MusicManager.download_next_song()

    @staticmethod
    async def play_song(ctx,song: VideoEntry,force: bool = False):
        """
        Try to play the given song.
        :param ctx: The context in which the command has been invoked
        :param song: The song to play
        :param force: If True then the bot will play the song directly Otherwise the song will be but into the song_queue
        """
        MusicManager.current_ctx = ctx

        if not force:
            if MusicManager.current_song:
                MusicManager.song_queue.append(song)
                if not MusicManager.next_song_entry:
                    MusicManager.next_song_index = 1
                    MusicManager.next_song_entry = MusicManager.song_queue[MusicManager.next_song_index]
                    await MusicManager.next_song_entry.download()
                return
            MusicManager.song_queue.append(song)

        MusicManager.current_song = song
        response = await MusicManager.current_song.play(ctx.voice_client)

        match response:
            case PlayResponse.SUCCESS:
                MusicManager.current_play_status = PlayStatus.PLAYING
                if not MusicManager.song_embed:
                    await MusicManager.send_song_embed(ctx,song)
                    if len(MusicManager.song_queue) > 1:
                        MusicManager.next_song_index = 1
                        MusicManager.next_song_entry = MusicManager.song_queue[1]
                        await MusicManager.next_song_entry.download()
            case PlayResponse.ANOTHER_SONG_IS_PLAYING:
                await MessageManager.send_error_message(ctx.channel,"Another song is already playing!")
            case PlayResponse.ERROR:
                await MessageManager.send_error_message(ctx.channel,"Error while trying to play the song!")

    async def pause_callback(interaction:discord.Interaction):
        """
        Pause the current song and switch pause button in song embed to the resume button
        :param interaction: The interaction that invoked this command
        """
        from voice.commands.PauseCommand import PauseCommand
        PauseCommand.pause(MusicManager.bot_voice_client)

        resume_button = discord.ui.Button(label=Emojis.RESUME,style=discord.ButtonStyle.primary)
        resume_button.callback = MusicManager.resume_callback

        MusicManager.song_view.remove_item(MusicManager.song_embed_buttons["pause/resume"])
        MusicManager.song_embed_buttons["pause/resume"] = resume_button
        MusicManager.song_view.add_item(MusicManager.song_embed_buttons["pause/resume"])

        await interaction.response.edit_message(embed=MusicManager.song_embed,view=MusicManager.song_view)

    async def resume_callback(interaction:discord.Interaction):
        """
        Resume the current song an switch the resume button in the song_embed to the pause button.
        :param interaction: The interaction that invoked this command
        """
        from voice.commands.ResumeCommand import ResumeCommand
        ResumeCommand.resume(MusicManager.bot_voice_client)

        pause_button = discord.ui.Button(label=Emojis.PAUSE,style=discord.ButtonStyle.primary)
        pause_button.callback = MusicManager.pause_callback

        MusicManager.song_view.remove_item(MusicManager.song_embed_buttons["pause/resume"])
        MusicManager.song_embed_buttons["pause/resume"] = pause_button
        MusicManager.song_view.add_item(MusicManager.song_embed_buttons["pause/resume"])

        await interaction.response.edit_message(embed=MusicManager.song_embed,view=MusicManager.song_view)

    async def stop_callback(interaction:discord.Interaction):
        """
        Stop the current song
        :param interaction: The interaction that invoked this command
        """
        from voice.commands.StopCommand import StopCommand
        await StopCommand.stop(MusicManager.bot_voice_client)
        await interaction.response.defer()

    async def skip_callback(interaction:discord.Interaction):
        """
        Skip the current song
        :param interaction: The interaction that invoked this command
        """
        if len(MusicManager.song_queue) <= 1 and not MusicManager.looping:
            await MusicManager.stop_callback(interaction)
            return

        MusicManager.bot_voice_client.stop()
        await interaction.response.defer()

    async def shuffle_callback(interaction:discord.Interaction):
        """
        Enables/Disables shuffling
        :param interaction: The interaction that invoked this command
        """
        MusicManager.shuffle = not MusicManager.shuffle
        MusicManager.song_embed_buttons["shuffle"].style = discord.ButtonStyle.green if MusicManager.shuffle else discord.ButtonStyle.red
        await interaction.response.edit_message(embed=MusicManager.song_embed,view=MusicManager.song_view)

    async def loop_callback(interaction:discord.Interaction):
        """
        Enables/Disables looping
        :param interaction: The interaction that invoked this command
        """
        MusicManager.looping = not MusicManager.looping
        MusicManager.song_embed_buttons["loop"].style = discord.ButtonStyle.green if MusicManager.looping else discord.ButtonStyle.red
        await interaction.response.edit_message(embed=MusicManager.song_embed, view=MusicManager.song_view)