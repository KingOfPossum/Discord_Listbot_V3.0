from database.Database import Database

class SongDatabase(Database):
    """
    Class to handle the database of songs, that saves when which song was played for the last time.
    """
    def __init__(self,folder_path):
        schema = """
        song_id TEXT PRIMARY KEY,
        last_played_time INTEGER    
        """

        super().__init__(folder_path=folder_path,
                         table_name="songs",
                         schema=schema)

    def add_song(self,song_id: str, last_played_time: int):
        """
        Add a song to the database.
        :param song_id: The ID of the song
        :param last_played_time: The last time the song was played
        """
        query = f"INSERT INTO {self.table_name} VALUES (?,?)"
        self.sql_execute(query,(song_id,last_played_time))

    def remove_song(self,song_id: str):
        """
        Remove a song from the database.
        :param song_id: The ID of the song
        """
        query = f"DELETE FROM {self.table_name} WHERE song_id = ?"
        self.sql_execute(query,(song_id,))

    def update_last_played_time(self,song_id: str, new_last_played_time: int):
        """
        Updates the last time the song was played.
        :param song_id: The ID of the song
        :param new_last_played_time:
        :return:
        """
        query = f"""
                UPDATE {self.table_name}
                SET last_played_time = ?
                WHERE song_id = ?
                """
        self.sql_execute(query,(new_last_played_time,song_id))

    def get_least_recently_played_song(self) -> str:
        """
        Get the song that was played the least recently.
        :return: The song ID of the least recently played song
        """
        query = f"""
                SELECT song_id
                FROM {self.table_name}
                ORDER BY last_played_time
                LIMIT 1
                """
        result = self.sql_execute_fetchall(query)
        return result[0][0] if result else None

    def get_all_songs(self) -> list[str]:
        """
        Get all songs from the database.
        :return: A list of all song IDs in the database
        """
        query = f"SELECT song_id FROM {self.table_name}"
        result = self.sql_execute_fetchall(query)
        return result

    def print_database(self):
        pass