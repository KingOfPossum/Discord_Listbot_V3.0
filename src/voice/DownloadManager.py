import asyncio
import re
import yt_dlp

from concurrent.futures import ThreadPoolExecutor
from common.ConfigLoader import ConfigLoader
from yt_dlp import DownloadError

class DownloadManager:
    """Class for managing the downloads of audio from YouTube"""

    executor = ThreadPoolExecutor(max_workers=4)

    youtube_options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{ConfigLoader.get_config().music_folder_path}%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    youtube_playlist_options = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'noplaylist': False,
        'extract_flat': True,
    }

    UNAVAILABLE_TITLES = {
        "[Private video]",
        "[Deleted video]",
        "Private video",
        "Deleted video",
        "This video is unavailable",
    }

    @staticmethod
    def extract_video_id_from_url(url: str) -> str:
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
    def search_for_video(query: str):
        """
        Searches YouTube for the given query.
        :param query: The query to search for.
        :return: A VideoEntry object containing relevant information about the video.
        """
        from voice.VideoEntry import VideoEntry

        with yt_dlp.YoutubeDL(DownloadManager.youtube_options) as ytdlp:
            info = ytdlp.extract_info(query, download=False)

            if not query.startswith("http"):
                if 'entries' in info:
                    result = info['entries'][0]
                    return VideoEntry.new(result['original_url'], result['title'], result['id'], result['duration'])

            return VideoEntry.new(info['original_url'], info['title'], info['id'], info['duration'])

    @staticmethod
    def search_for_playlist(query: str):
        """
        Searches YouTube for a playlist matching the given query.
        :param query: The query to search for.
        :return: A list of VideoEntry objects representing the videos in the playlist.
        """
        from voice.VideoEntry import VideoEntry

        with yt_dlp.YoutubeDL(DownloadManager.youtube_playlist_options) as ytdlp:
            info = ytdlp.extract_info(query, download=False)

            video_entries = []
            if 'entries' in info:
                for entry in info['entries']:
                    title = entry['title']
                    if not title or title in DownloadManager.UNAVAILABLE_TITLES:
                        print(f"Found unavailable or private video in playlist, skipping: {title}")
                        continue
                    availability = entry.get("availability")
                    if availability in ("unavailable", "private", "needs_auth", "subscriber_only"):
                        print(f"Found unavailable or private video in playlist, skipping: {title}")
                        continue
                    if entry.get("_type") == "url" and len(entry.keys()) <= 3:
                        print(f"Found unavailable or private video in playlist, skipping: {title}")
                        continue

                    video_entries.append(VideoEntry.new(entry['url'], entry['title'], entry['id'], entry['duration']))

            return video_entries

    @staticmethod
    async def download_audio_from_url(url):
        """
        Downloads the audio from a YouTube URL.
        :param url: The URL of the YouTube video.
        """
        try:
            with yt_dlp.YoutubeDL(DownloadManager.youtube_options) as ydl:
                future = asyncio.get_running_loop().run_in_executor(DownloadManager.executor, lambda:ydl.download([url]))
                await future

                return True
        except DownloadError as e:
            print(f"Error downloading audio from URL {url}: {e}")
            return False
        except Exception:
            return False