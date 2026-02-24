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

    def print_database(self):
        pass