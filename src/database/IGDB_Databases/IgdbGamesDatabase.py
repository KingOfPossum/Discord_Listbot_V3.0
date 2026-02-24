from common.IGDBGameEntry import IGDBGameEntry
from database.Database import Database

class IGDBGamesDatabase(Database):
    def __init__(self,folder_path: str):
        schema = """
        game_id INTEGER,
        game_name TEXT NOT NULL,
        cover_url TEXT,
        summary TEXT,        
        PRIMARY KEY (game_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="igdb_games",
                         schema=schema)

    def insert_game(self,igdb_entry: IGDBGameEntry):
        """
        Inserts a game entry into the database.
        :param igdb_entry: The IGDBGameEntry object containing the game information to be inserted into the database.
        """
        query = f"INSERT INTO {self.table_name} VALUES (game_id,game_name,cover_url,summary) VALUES (?,?,?,?)"
        self.sql_execute(query,(igdb_entry.game_id,igdb_entry.game_name,igdb_entry.cover_url,igdb_entry.summary))

    def game_exists(self, game_id:int) -> bool:
        """
        Checks if a game with the given game_id already exists in the database.
        :param game_id: The ID of the game to check for existence.
        :return: True if the game exists in the database, False otherwise.
        """
        query = f"SELECT * FROM {self.table_name} WHERE game_id = ?"
        result = self.sql_execute_fetchall(query, (game_id,))
        return len(result) > 0

    def print_database(self):
        pass