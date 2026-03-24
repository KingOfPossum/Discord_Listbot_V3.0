import os

from common.ConfigLoader import ConfigLoader

def get_music_folder_size() -> int:
    """
    Calculates the total size of the music folder in bytes
    :return: The total size of the music folder in bytes
    """
    music_folder_path = ConfigLoader.get_config().music_folder_path

    total_size = 0
    for root,dirs,files in os.walk(music_folder_path):
        for file in files:
            total_size += os.path.getsize(os.path.join(root,file))
    print(total_size)

    return total_size

def delete_song(song: str):
    """
    Will delete the given song from the music folder.
    :param song: The name of the song / the file name.
    """
    music_folder_path = ConfigLoader.get_config().music_folder_path
    song_path = os.path.join(music_folder_path, song + ".mp3")

    try:
        os.remove(song_path)
    except FileNotFoundError:
        print("Song file not found.")

def check_for_delete():
    """
    Checks if the size of the music folder exceeds the specified size in the config.
    If it does it will choose a song and delete it.
    """
    if get_music_folder_size() > ConfigLoader.get_config().max_music_folder_size:
        # look into a database for the least recently used song and delete it
        pass