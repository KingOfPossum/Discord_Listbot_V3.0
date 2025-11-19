import re
import yt_dlp

from common.ConfigLoader import ConfigLoader

class DownloadManager:
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
                    video_entries.append(VideoEntry.new(entry['url'], entry['title'], entry['id'], entry['duration']))

            return video_entries

    @staticmethod
    def download_audio_from_url(url):
        """
        Downloads the audio from a YouTube URL.
        :param url: The URL of the YouTube video.
        """
        with yt_dlp.YoutubeDL(DownloadManager.youtube_options) as ydl:
            ydl.download([url])