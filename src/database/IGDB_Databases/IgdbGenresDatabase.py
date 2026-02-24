from database.Database import Database

class IGDBGenresDatabase(Database):
    def __init__(self, folder_path: str):
        schema = """
        genre_id INTEGER,
        genre_name TEXT NOT NULL,
        PRIMARY KEY (genre_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="igdb_genres",
                         schema=schema)

    def print_database(self):
        pass