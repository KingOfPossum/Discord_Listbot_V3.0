from database.Database import Database

class IGDBGamePlatformDatabase(Database):
    def __init__(self,folder_path: str):
        schema = """
        game_id INTEGER,
        platform_id INTEGER,
        PRIMARY KEY (game_id,platform_id),
        FOREIGN KEY (game_id) REFERENCES igdb_games(game_id),
        FOREIGN KEY (platform_id) REFERENCES igdb_platforms(platform_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="igdb_games_platforms",
                         schema=schema)

    def add_game_platform(self, game_id: int, platform_id: int):
        """
        Adds a game-platform relationship to the database.
        :param game_id: The ID of the game to be added to the database.
        :param platform_id: The ID of the platform to be added to the database.
        """
        query = f"INSERT INTO {self.table_name} (game_id, platform_id) VALUES (?, ?)"
        self.sql_execute(query, (game_id, platform_id))

    def print_database(self):
        pass