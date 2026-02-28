from common.IGDBGameEntry import IGDBGameEntry
from database.IGDB_Databases.IgdbGameGenreDatabase import IGDBGameGenreDatabase
from database.IGDB_Databases.IgdbGamePlatformDatabase import IGDBGamePlatformDatabase
from database.IGDB_Databases.IgdbGamesDatabase import IGDBGamesDatabase
from database.IGDB_Databases.IgdbGenresDatabase import IGDBGenresDatabase
from database.IGDB_Databases.IgdbPlatformsDatabase import IGDBPlatformsDatabase

class IGDBDatabaseCollection:
    def __init__(self,folder_path: str):
        self.folder_path = folder_path
        self.database_path = folder_path + "/database.db"
        self.games_database = IGDBGamesDatabase(folder_path)
        self.genres_database = IGDBGenresDatabase(folder_path)
        self.platforms_database = IGDBPlatformsDatabase(folder_path)
        self.game_genre_database = IGDBGameGenreDatabase(folder_path)
        self.game_platform_database = IGDBGamePlatformDatabase(folder_path)

    def add_game(self, igdb_entry: IGDBGameEntry):
        """
        Adds a game to the database collection. This will add the game to the games database, and also add the relevant entries to the genres and platforms databases,
        as well as the game-genre and game-platform databases.
        :param igdb_entry: The IGDBGameEntry object representing the game to be added to the database collection.
        """
        if self.game_exists_by_id(igdb_entry.game_id):
            return

        self.games_database.insert_game(igdb_entry)

        genre_ids = []
        for genre in igdb_entry.genres:
            genre_ids.append(self.add_genre(genre))

        platform_ids = []
        for platform in igdb_entry.platforms:
            platform_ids.append(self.add_platform(platform))

        for genre_id in genre_ids:
            self.game_genre_database.add_game_genre(igdb_entry.game_id, genre_id)

        for platform_id in platform_ids:
            self.game_platform_database.add_game_platform(igdb_entry.game_id, platform_id)

    def get_entry_by_id(self,game_id: int) -> IGDBGameEntry | None:
        """
        Gets a IGDBGameEntry object representing the game with the given game_id from the database collection.
        :param game_id: The ID of the game to get from the database collection.
        :return: The IGDBGameEntry object representing the game with the given game_id from the database collection, or None if the game does not exist in the database collection.
        """
        if not self.game_exists_by_id(game_id):
            return None

        query = "SELECT * FROM igdb_games WHERE game_id = ?"
        result = self.games_database.sql_execute_fetchall(query,(game_id,))[0]
        genres = self.get_genres(game_id)
        platforms = self.get_platforms(game_id)

        return IGDBGameEntry(result[0],result[1],result[2],result[3],genres,platforms)

    def get_entry_by_name(self,game_name: str) -> IGDBGameEntry | None:
        """
        Gets a IGDBGameEntry object representing the game with the given game_name from the database collection.
        :param game_name: The name of the game to get from the database collection.
        :return: The IGDBGameEntry object representing the game with the given game_name from the database collection, or None if the game does not exist in the database collection.
        """
        game_id = self.game_exists_by_name(game_name)
        if not game_id:
            return None

        return self.get_entry_by_id(game_id)

    def add_genre(self, genre_name: str) -> int:
        """
        Adds a genre to the database collection. This will add the genre to the genres database.
        Will also return the genre_id of the genre, whether it was newly added or already existed in the database collection.
        :param genre_name: The name of the genre to be added to the database collection.
        :returns: The genre_id of the genre, whether it was newly added or already existed in the database collection.
        """
        genre_id = self.genre_exists(genre_name)
        if genre_id:
            return genre_id

        return self.genres_database.add_genre(genre_name)

    def add_platform(self, platform_name: str) -> int:
        """
        Adds a platform to the database collection. This will add the platform to the platforms database.
        :param platform_name: The name of the platform to be added to the database collection.
        """
        platform_id = self.platform_exists(platform_name)
        if platform_id:
            return platform_id

        return self.platforms_database.add_platform(platform_name)

    def game_exists_by_id(self, game_id: int) -> bool:
        """
        Checks if a game is already in the database collection by checking if the game ID exists in the games database.
        :param game_id: The ID of the game to check for in the database collection.
        :return: True if the game is already in the database collection, False otherwise.
        """
        return self.games_database.game_exists_by_id(game_id)

    def game_exists_by_name(self, game_name: str) -> int | None:
        """
        Checks if a game is already in the database collection by checking if the game name exists in the games database.
        :param game_name: The name of the game to check for in the database collection.
        :return: The game_id of the game if it is already in the database collection, None otherwise.
        """
        return self.games_database.game_exists_by_name(game_name)

    def genre_exists(self, genre_name: str) -> int | None:
        """
        Checks if a genre is already in the database collection by checking if the genre name exists in the genres database.
        Returns the genre_id if the genre exists, None otherwise.
        :param genre_name: The name of the genre to check for in the database collection.
        :return: The genre_id of the genre if it is already in the database collection, None otherwise.
        """
        return self.genres_database.genre_exists(genre_name)

    def platform_exists(self, platform_name: str) -> int | None:
        """
        Checks if a platform is already in the database collection by checking if the platform name exists in the platforms database.
        Returns the platform_id if the platform exists, None otherwise.
        :param platform_name: The name of the platform to check for in the database collection.
        :return: The platform_id of the platform if it is already in the database collection, None otherwise.
        """
        return self.platforms_database.platform_exists(platform_name)

    def get_genres(self, game_id:int) -> list[str]:
        """
        Get all genre_names that correspond to a game_id
        :param game_id: The ID of the game to get the genres for.
        :return: The list of genre_names that correspond to the game_id.
        """
        query = """
                SELECT genre_name
                FROM igdb_genres JOIN igdb_games_genres ON igdb_genres.genre_id = igdb_games_genres.genre_id
                WHERE game_id = ?
                """

        result = self.genres_database.sql_execute_fetchall(query,(game_id,))
        return [genre[0] for genre in result]

    def get_platforms(self, game_id:int) -> list[str]:
        """
        Get all platform_names that correspond to a game_id
        :param game_id: The ID of the game to get the platforms for.
        :return: The list of platform_names that correspond to the game_id.
        """
        query = """
                SELECT platform_name
                FROM igdb_platforms JOIN igdb_games_platforms ON igdb_platforms.platform_id = igdb_games_platforms.platform_id
                WHERE game_id = ?
                """

        result = self.platforms_database.sql_execute_fetchall(query,(game_id,))
        return [platform[0] for platform in result]