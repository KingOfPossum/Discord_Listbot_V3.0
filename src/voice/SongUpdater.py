from discord.ext import commands, tasks
from voice.MusicManager import MusicManager
from voice.PlayStatus import PlayStatus
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

    @tasks.loop(seconds=1)
    async def update(self):
        await self._update_song_embed()
        await self.check_for_inactivity()

    @update.before_loop
    async def before_track_time(self):
        """This will ensure that the TimeTracker only starts after the bot is ready."""
        await self.bot.wait_until_ready()

    @staticmethod
    async def _update_song_embed():
        if MusicManager.current_song and MusicManager.song_embed and MusicManager.song_message:
            if MusicManager.current_play_status == PlayStatus.PLAYING:
                MusicManager.current_song.current_playtime += 1
                MusicManager.song_embed.description = f"{VoiceUtils.convert_seconds_to_time(MusicManager.current_song.current_playtime)} - {VoiceUtils.convert_seconds_to_time(MusicManager.current_song.duration)}"
                await MusicManager.song_message.edit(embed=MusicManager.song_embed)

    async def check_for_inactivity(self):
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