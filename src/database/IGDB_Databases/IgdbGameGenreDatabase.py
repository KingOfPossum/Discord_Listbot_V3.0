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

    def add_game_genre(self, game_id: int, genre_id: int):
        """
        Adds a game-genre relationship to the database.
        :param game_id: The ID of the game to be added to the database.
        :param genre_id: The ID of the genre to be added to the database.
        """
        query = f"INSERT INTO {self.table_name} (game_id, genre_id) VALUES (?, ?)"
        self.sql_execute(query, (game_id, genre_id))

    def print_database(self):
        pass