import os

from common.ConfigLoader import ConfigLoader
from database.DatabaseCollection import DatabaseCollection

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

    return total_size

def delete_song(song: str):
    """
    Will delete the given song from the music folder.
    :param song: The name of the song / the file name.
    """
    music_folder_path = ConfigLoader.get_config().music_folder_path
    song_path = os.path.join(music_folder_path, song)

    try:
        os.remove(song_path)
    except FileNotFoundError:
        print("Song file not found.",song_path)

def check_if_song_database_is_correct():
    """
    Checks for every song in the database if the corresponding file still exists.
    If not it removes the entry from the database as the database is no longer correct.
    """
    music_folder_path = ConfigLoader.get_config().music_folder_path

    songs_in_database = [song[0] for song in DatabaseCollection.song_database.get_all_songs()]

    for root,dirs,files in os.walk(music_folder_path):
        for file in files:
            file = file[:-4]
            print(file)

            if file in songs_in_database:
                songs_in_database.remove(file)

    for song in songs_in_database:
        DatabaseCollection.song_database.remove_song(song)

def check_for_delete():
    """
    Checks if the size of the music folder exceeds the specified size in the config.
    If it does it will choose a song and delete it.
    """
    check_if_song_database_is_correct()

    if get_music_folder_size() > ConfigLoader.get_config().max_music_folder_size:
        least_recently_played_song = DatabaseCollection.song_database.get_least_recently_played_song()
        delete_song(least_recently_played_song + ".mp3")
        DatabaseCollection.song_database.remove_song(least_recently_played_song)
        print("Song deleted. ",least_recently_played_song + ".mp3")

        check_for_delete()
