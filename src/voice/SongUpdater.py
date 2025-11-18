from discord.ext import commands, tasks
from voice.MusicManager import MusicManager
from voice.enums.PlayStatus import PlayStatus
from voice.VoiceUtils import VoiceUtils

class SongUpdater(commands.Cog):
    """
    Cog for updating voice stuff like the song embeds
    """
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        """Is executed when the TimeTracker cog is loaded"""
        self.update.start()
        print("Voice updater loaded")

    async def cog_unload(self):
        """Is executed when the TimeTracker cog is unloaded"""
        self.update.cancel()
        print("Voice updater unloaded")

    @tasks.loop(seconds=1,reconnect=True)
    async def update(self):
        await self._update_song_embed()
        await self.check_for_inactivity()

    @update.before_loop
    async def before_track_time(self):
        """This will ensure that the TimeTracker only starts after the bot is ready."""
        await self.bot.wait_until_ready()

    @staticmethod
    async def _update_song_embed():
        """
        Updates the song embed. Updating the current playtime in the embed
        """
        if MusicManager.current_song and MusicManager.song_embed and MusicManager.song_message:
            print(f"\nCurrent Song: {MusicManager.current_song.title}")
            print(f"Song queue: {[song.title for song in MusicManager.song_queue]}")
            print(f"Current song index: {MusicManager.current_song_index}")
            print(f"Looping: {MusicManager.looping}")
            print(f"Shuffle: {MusicManager.shuffle}\n")

            if MusicManager.current_play_status == PlayStatus.PLAYING:
                MusicManager.current_song.current_playtime += 1
                MusicManager.song_embed.description = f"[{MusicManager.current_song.title}]({MusicManager.current_song.url})\n{VoiceUtils.convert_seconds_to_time(MusicManager.current_song.current_playtime)} - {VoiceUtils.convert_seconds_to_time(MusicManager.current_song.duration)}"
                MusicManager.song_embed.set_thumbnail(url=MusicManager.current_song.thumbnail_url)
                await MusicManager.song_message.edit(embed=MusicManager.song_embed)

    async def check_for_inactivity(self):
        """
        Checks how long the bot has been inactive in a voice chat.
        Being to loong inactive results in the bot being kicked from the voice chat.
        :return:
        """
        print(f"Inactivity check : Inactive for {MusicManager.inactive_time} seconds")
        if MusicManager.current_play_status == PlayStatus.PLAYING:
            MusicManager.reset_inactivity()
        else:
            if len(self.bot.voice_clients) > 0:
                MusicManager.inactive_time += 1

                if MusicManager.inactive_time > MusicManager.INACTIVE_SECONDS_UNTIL_DISCONNECT:
                    print("Disconnected from voice due to inactivity")
                    MusicManager.reset_inactivity()
                    await MusicManager.delete_song_message()
                    await self.bot.voice_clients[0].disconnect()
            else:
                MusicManager.reset_inactivity()