from Database import Database

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
        query = f"INSERT INTO {self.table_name} VALEUS (?,?)"
        self.sql_execute(query,(song_id,last_played_time))

    def remove_song(self,song_id: str):
        query = f"DELETE FROM {self.table_name} WHERE song_id = ?"
        self.sql_execute(query,(song_id,))

    def update_last_played_time(self,song_id: str, new_last_played_time: int):
        query = f"""
                UPDATE {self.table_name}
                SET last_played_time = ?
                WHERE song_id = ?
                """
        self.sql_execute(query,(new_last_played_time,song_id))

    def get_least_recently_played_song(self):
        query = f"""
                SELECT song_id
                FROM {self.table_name}
                ORDER BY last_played_time
                LIMIT 1
                """
        result = self.sql_execute_fetchall(query)
        return result[0] if result else None

    def print_database(self):
        pass