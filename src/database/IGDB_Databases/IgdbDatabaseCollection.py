from common.IGDBGameEntry import IGDBGameEntry
from database.IGDB_Databases.IgdbGameGenreDatabase import IGDBGameGenreDatabase
from database.IGDB_Databases.IgdbGamePlatformDatabase import IGDBGamePlatformDatabase
from database.IGDB_Databases.IgdbGamesDatabase import IGDBGamesDatabase
from database.IGDB_Databases.IgdbGenresDatabase import IGDBGenresDatabase
from database.IGDB_Databases.IgdbPlatformsDatabase import IGDBPlatformsDatabase

class IGDBDatabaseCollection:
    def __init__(self,folder_path: str):
        self.games_database = IGDBGamesDatabase(folder_path)
        self.genres_database = IGDBGenresDatabase(folder_path)
        self.platforms_database = IGDBPlatformsDatabase(folder_path)
        self.game_genre_database = IGDBGameGenreDatabase(folder_path)
        self.game_platform_database = IGDBGamePlatformDatabase(folder_path)

    def addGame(self, igdb_entry: IGDBGameEntry):
        """
        Adds a game to the database collection. This will add the game to the games database, and also add the relevant entries to the genres and platforms databases,
        as well as the game-genre and game-platform databases.
        :param igdb_entry: The IGDBGameEntry object representing the game to be added to the database collection.
        """
        if self.game_exists(igdb_entry.game_id):
            return

        self.games_database.insert_game(igdb_entry)

    def game_exists(self, game_id: int) -> bool:
        """
        Checks if a game is already in the database collection by checking if the game ID exists in the games database.
        :param game_id: The ID of the game to check for in the database collection.
        :return: True if the game is already in the database collection, False otherwise.
        """
        return self.games_database.game_exists(game_id)