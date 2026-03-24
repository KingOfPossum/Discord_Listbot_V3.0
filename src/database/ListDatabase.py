from dataclasses import astuple
from common.GameEntry import GameEntry
from common.UserManager import UserManager
from database.Database import Database

class ListDatabase(Database):
    """
    A class to handle database operations for a list of games using SQLite3.
    """
    def __init__(self,folder_path: str):
        schema = """
        game_id INTEGER,
        igdb_game_id INTEGER,
        user_id INTEGER,
        name TEXT NOT NULL,
        date DATE NOT NULL,
        console TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK(rating BETWEEN 0 AND 100),
        review TEXT,
        replay INTEGER DEFAULT 0 CHECK(replay IN (0, 1)),
        hundred_percent INTEGER DEFAULT 0 CHECK(hundred_percent IN (0, 1)),
        PRIMARY KEY (game_id),
        FOREIGN KEY (igdb_game_id) REFERENCES igdb_games(game_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        UNIQUE (user_id, name, date)
        """

        super().__init__(folder_path=folder_path,
                         table_name="games",
                         schema=schema)

    def game_already_in_database(self,entry: GameEntry) -> bool:
        """
        Checks if a game entry is already in the database.
        This method will search for an entry with the same name and user in the database.
        :param entry: The GameEntry object to be checked.
        :return: True if the game entry is already in the database, False otherwise.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ? AND name = ? AND date = ?"
        data = self.sql_execute_fetchall(query, (entry.user_id,entry.name,entry.date))

        return len(data) > 0

    def get_game_entry(self,name: str, user_id: int) -> GameEntry | None:
        """
        Retrieves a game entry from the database based on the name and user.
        Will return the newest added entry if game exists multiple times.
        :param name: The name of the game.
        :param user_id: The ID of the user who added the game.
        :return: A GameEntry object containing the details of the game.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ? AND name = ? ORDER BY game_id DESC"
        data = self.sql_execute_fetchall(query, (user_id, name))

        if not data:
            return None

        return GameEntry(*data[0])

    def get_game_entry_by_id(self,game_id: int) -> GameEntry | None:
        """
        Retrieves a game entry from the database based on the unique game ID.
        :param game_id: The unique ID of the game.
        :return: The GameEntry object containing the details of the game, or None if not found.
        """
        query = f"SELECT * FROM {self.table_name} WHERE game_id = ?"
        data = self.sql_execute_fetchall(query, (game_id,))

        if not data:
            return None

        return GameEntry(*data[0])

    def get_all_instances_of_game(self,name: str, user_id: int) -> list[GameEntry] | None:
        """
        Retrieves all instances of a game entry from the database based on the name and user sorted by the date they were added.
        :param name: Name of the game
        :param user_id:The ID of the user who added the game
        :return: A list of GameEntry objects containing the details of all instances of the game added by the user sorted by date.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ? AND name = ? ORDER BY date DESC"
        data = self.sql_execute_fetchall(query, (user_id, name))

        return [GameEntry(*row) for row in data] if data else None

    def get_all_game_entries(self,user_id:int=None,year:str=None) -> list[GameEntry]:
        """
        Retrieves all game entries from the database.
        Optionally filters for specific users or a specific year if userid/year is provided.
        :param user_id: The ID of the user whose game entries are to be retrieved. If None retrieves all users' entries.
        :param year: The year to filter the game entries. If None, retrieves the entries from all years.
        :return: A list of all GameEntry objects in the database.
        """
        #query for year and user if year/user is given otherwise a query that is always true so that the real query still works
        year_filter = f"STRFTIME('%Y',date) = '{year}'" if year else "1=1"
        user_filter = f"user_id = '{user_id}'" if user_id else "1=1"

        query = f"SELECT * FROM {self.table_name} WHERE {year_filter} AND {user_filter}"
        data = self.sql_execute_fetchall(query)

        return [GameEntry(*row) for row in data]

    def put_game(self, entry: GameEntry):
        """
        Adds a game entry into the database.
        If the game already exists, updates its information.
        :param entry: The GameEntry object containing the details of the game to be added.
        """
        query = f"""
            INSERT INTO {self.table_name} (igdb_game_id,user_id,name,date,console,rating,review,replay,hundred_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (user_id, name, date)
            DO UPDATE SET
                igdb_game_id = excluded.igdb_game_id,
                console = excluded.console,
                rating = excluded.rating,
                review = excluded.review,
                replay = excluded.replay,
                hundred_percent = excluded.hundred_percent
            """
        self.sql_execute(query, astuple(entry)[1:])

    def remove_entry(self,entry: GameEntry):
        """
        Removes a game entry from the database based on the name, user, and date.
        :param entry: The GameEntry object to be removed from the database.
        """
        query = f"DELETE FROM {self.table_name} WHERE name = ? AND user_id = ? AND date = ?"
        self.sql_execute(query, (entry.name, entry.user_id, entry.date))

    def remove_entry_by_id(self,game_id: int):
        """
        Removes a game entry from the database based on its id.
        :param game_id: The ID of the game entry to be removed.
        """
        query = f"DELETE FROM {self.table_name} WHERE game_id = ?"
        self.sql_execute(query,(game_id,))

    def get_years(self,user_id: int = None) -> list[str]:
        """
        Retrieves a list of distinct years in which the user has added games.
        :param user_id: The ID of the user whose game years are to be retrieved, if user is None consider all games added by all users in total resulting in retrieving all years that exist in the database.
        :return: A list of years as strings.
        """
        user_filter = f"user_id = '{user_id}'" if user_id is not None else "1=1"

        query = f"SELECT DISTINCT STRFTIME('%Y',date) AS year FROM {self.table_name} WHERE {user_filter} ORDER BY year DESC"
        data = self.sql_execute_fetchall(query)

        return [row[0] for row in data if row[0] is not None]

    def does_user_have_entries(self,user_id: int) -> bool:
        """
        Checks if a user has any game entries in the database.
        :param user_id: The ID of the user to check for
        :return: True if the user has at least one game entry, False otherwise.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ?"
        data = self.sql_execute_fetchall(query, (user_id,))

        return len(data) > 0

    def get_highest_rated_games(self,user_id: int = None,year:int = None, limit: int = 3) -> list[tuple[str,int]]:
        """
        Retrieves the highest rated games for a specific user, limited to a specified number of entries from a specific year.
        If no user_id is provided, retrieves the highest rated games across all users.
        If no year is provided, retrieves the highest rated games from all years.
        :param user_id: The ID of the user whose highest rated games are to be retrieved.
        :param year: The year to filter the game entries.
        :param limit: The number of games to retrieve, default is 3.
        :return: A list of Tuples containing the name and rating of the highest rated games for the specified user.
        """
        user_filter = f"user_id = '{user_id}'" if user_id else "1=1"
        year_filter = f"STRFTIME('%Y',date) = '{year}'" if year else "1=1"

        query = f"SELECT name,rating FROM {self.table_name} WHERE {user_filter} AND {year_filter} ORDER BY rating DESC LIMIT ?"

        return self.sql_execute_fetchall(query, (limit,))

    def get_worst_rated_games(self,user_id: int = None,year:int = None,limit: int = 3) -> list[tuple[str,int]]:
        """
        Retrieves the worst rated games for a specific user, limited to a specified number of entries.
        If no user_id is provided, retrieves the worst rated games across all users.
        :param user_id: The ID of the user whose worst rated games are to be retrieved.
        :param year: The year to filter the game entries.
        :param limit: The number of games to retrieve, default is 3.
        :return: A list of Tuples containing the name and rating of the worst rated games for the specified user.
        """
        user_filter = f"user_id = '{user_id}'" if user_id else "1=1"
        year_filter = f"STRFTIME('%Y',date) = '{year}'" if year else "1=1"

        query = f"SELECT name,rating FROM {self.table_name} WHERE {user_filter} AND {year_filter} ORDER BY rating LIMIT ?"

        return self.sql_execute_fetchall(query, (limit,))

    def get_user_game_counts(self,year:int = None,limit:int = 3) -> list[tuple[str,int]]:
        """
        Retrieves for all users the number of games they have added to the database.
        If a year is provided, only counts the games added in that year.
        :param year: The year to filter the game entries.
        :param limit: The number of games to retrieve, default is 3.
        :return: A list of tuples containing the user ID and the corresponding count of games added by that user, sorted by count in descending order.
        """
        year_filter = f"STRFTIME('%Y',date) = '{year}'" if year else "1=1"
        query = f"""
                SELECT user_id, COUNT(*) as game_count
                FROM {self.table_name}
                WHERE {year_filter}
                GROUP BY user_id
                ORDER BY game_count DESC
                LIMIT ?
                """
        result = self.sql_execute_fetchall(query, (limit,))

        return [(UserManager.get_user_entry(user_id=user_id).display_name,game_count) for user_id,game_count in result]

    def get_months_counts(self,user_id:int = None,year:int = None,limit:int = 3) -> list[tuple[str,int]]:
        """
        Retrieves the number of games added to the database for each month of a specific year.
        If no year is provided, retrieves the counts for all months across all years.
        :param user_id: The ID of the user whose counts are to be retrieved.
        :param year: The year to filter the game entries.
        :param limit: The number of games to retrieve, default is 3.
        :return: A list of tuples containing the month and the corresponding count of games added in that month, sorted by the number of games.
        """
        user_filter = f"user_id = '{user_id}'" if user_id else "1=1"
        year_filter = f"STRFTIME('%Y',date) = '{year}'" if year else "1=1"

        query = f"""
                SELECT STRFTIME('%m', date) AS month, COUNT(*) as game_count
                FROM {self.table_name}
                WHERE {year_filter} AND {user_filter}
                GROUP BY month
                ORDER BY game_count DESC
                LIMIT ?
                """
        result = self.sql_execute_fetchall(query,(limit,))

        num_to_month = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
        return [(num_to_month.get(month, "Unknown"), game_count) for month, game_count in result]

    def get_console_counts(self,user_id:int = None,year:int = None,limit:int = 3) -> list[tuple[str,int]]:
        """
        Retrieves the number of games added to the database for each console in a specific year.
        If no year is provided, retrieves the counts for all consoles across all years.
        :param user_id: The ID of the user.
        :param year: The year to filter the game entries.
        :param limit: The number of consoles to retrieve, default is 3.
        :return: A list of tuples containing the console and the corresponding count of games added for that console, sorted by the number of games.
        """
        user_filter = f"user_id = '{user_id}'" if user_id else "1=1"
        year_filter = f"STRFTIME('%Y',date) = '{year}'" if year else "1=1"

        query = f"""
                SELECT console, COUNT(*) as game_count
                FROM {self.table_name}
                WHERE {year_filter} AND {user_filter}
                GROUP BY console
                ORDER BY game_count DESC
                LIMIT ?
                """
        return self.sql_execute_fetchall(query,(limit,))

    def get_genre_counts(self,user_id:int = None,year:int = None,limit:int = 3) -> list[tuple[str,int]]:
        """
        Retrieves the number of games added to the database for each genre in a specific year for a specific user.
        If no year is provided, retrieves the counts for all genres across all years.
        If no user_id is provided, retrieves the counts for all users.
        :param user_id: The ID of the user to retrieve the genre counts for.
        :param year: The year to filter the game entries.
        :param limit: The number of genres to retrieve, default is 3.
        :return: A list of tuples containing the genre and the corresponding count of games added for that genre, sorted by the number of games.
        """
        from database.DatabaseCollection import DatabaseCollection

        user_filter = f"user_id = '{user_id}'" if user_id else "1=1"
        year_filter = f"STRFTIME('%Y',date) = '{year}'" if year else "1=1"

        query = f"""
                SELECT genre_name, COUNT(*) as games_count
                FROM {self.table_name} games
                JOIN {DatabaseCollection.igdb_databases.games_database.table_name} igdb ON games.igdb_game_id = igdb.game_id
                JOIN {DatabaseCollection.igdb_databases.game_genre_database.table_name} games_genres ON igdb.game_id = games_genres.game_id
                JOIN {DatabaseCollection.igdb_databases.genres_database.table_name} genres ON games_genres.genre_id = genres.genre_id
                WHERE {year_filter} AND {user_filter}
                GROUP BY genre_name
                ORDER BY games_count DESC
                LIMIT ?
                """
        return self.sql_execute_fetchall(query, (limit,))

    def print_database(self):
        """Prints the contents of the database to the console."""
        print("-"*100 + "\nDatabase: " + self._path + "\n" + "-"*100)

        data = self.sql_execute_fetchall(f"SELECT * FROM {self.table_name}")

        print("Database contains " + str(len(data)) + " entries:")

        for row in data:
            print(" - " + str(row))

        print("-"*100 + "\n")