import os

from voice.VideoEntry import VideoEntry

class MusicManager:
    current_song: VideoEntry = None

    def __init__(self,music_folder_path: str):
        self.create_music_folder_if_not_exists(music_folder_path)

    @staticmethod
    def create_music_folder_if_not_exists(music_folder_path: str):
        if not os.path.exists(music_folder_path):
            print(f"Creating music folder at {music_folder_path}")
            os.mkdir(music_folder_path)