import asyncio
import dataclasses
import os

from common.BootLoop import BotLoop
from common.ConfigLoader import ConfigLoader
from discord import VoiceClient, FFmpegPCMAudio
from voice.DownloadManager import DownloadManager
from voice.enums.PlayResponse import PlayResponse
from voice.enums.PlayStatus import PlayStatus

@dataclasses.dataclass
class VideoEntry:
    """
    Represents a video entry with following properties:
     url : The url of the video.\n
     title : The title of the video.\n
     video_id : The id of the video.\n
     duration: The duration of the video.\n
     current_playtime : How long has the video been played.\n
     thumbnail_url : The url of the thumbnail of the video.
    """
    url: str
    title: str
    video_id: str
    duration: int
    current_playtime: int
    thumbnail_url: str
    file_path: str
    downloaded: bool

    @classmethod
    def new(cls,url,title,video_id,duration):
        """
        Creates a new VideoEntry object.
        :param url: The url of the video. Also used to create the thumbnail_url.
        :param title: The title of the video.
        :param video_id: The id of the video.
        :param duration: The duration of the video.
        :return: A new VideoEntry object.
        """
        file_path = ConfigLoader.get_config().music_folder_path + video_id + ".mp3"
        already_downloaded = os.path.exists(file_path)

        return cls(url,title,video_id,duration,0,f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",file_path,already_downloaded)

    async def play(self,bot_voice:VoiceClient):
        """
        Plays the audio from this VideoEntry object.
        :param bot_voice: The VoiceClient object of the bot used to play the audio.
        :return: PlayResponse object representing if the playing was successful.
        """
        from voice.MusicManager import MusicManager

        if MusicManager.current_play_status == PlayStatus.PLAYING:
            return PlayResponse.ANOTHER_SONG_IS_PLAYING

        if not self.downloaded:
            await self.download()
            self.downloaded = True

        self.current_playtime = 0
        source = FFmpegPCMAudio(self.file_path)
        bot_voice.play(source,after=lambda _: asyncio.run_coroutine_threadsafe(MusicManager.next_song(),BotLoop.loop))
        return PlayResponse.SUCCESS

    async def download(self):
        """
        Downloads the audio from this VideoEntry object.
        :return:
        """
        if not self.downloaded:
            print(f"DOWNLOADING AUDIO FOR SONG : {self.title}")
            if await DownloadManager.download_audio_from_url(url=self.url):
                self.downloaded = True
                return True
            else:
                print("DOWNLOAD FAILED: PROBABLY VIDEO UNAVAILABLE")
                return False
        return True

    def __str__(self):
        return f"URL: {self.url}\nTitle: {self.title}\nVideo ID: {self.video_id}\nThumbnail URL: {self.thumbnail_url}\nDuration: {self.duration}\nDownloaded: {self.downloaded}"