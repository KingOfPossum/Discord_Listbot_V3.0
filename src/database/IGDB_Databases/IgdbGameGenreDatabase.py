from database.Database import Database

class IGDBGameGenreDatabase(Database):
    def __init__(self,folder_path: str):
        schema = """
        game_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY (game_id,genre_id),
        FOREIGN KEY (game_id) REFERENCES igdb_games(game_id),
        FOREIGN KEY (genre_id) REFERENCES igdb_genres(genre_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="igdb_games_genres",
                         schema=schema)

    def print_database(self):
        pass