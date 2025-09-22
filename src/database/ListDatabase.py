from common.GameEntry import GameEntry
from database.Database import Database

class ListDatabase(Database):
    """
    A class to handle database operations for a list of games using SQLite3.
    """
    def __init__(self,folder_path: str):
        super().__init__(folder_path=folder_path,
                         database_name="list",
                         table_name="games",
                         params=[("name","TEXT"), ("user","TEXT"),("date","DATE"),("console","TEXT"),("rating","INT"),("review","TEXT"),("cover","TEXT"),("replay","INTEGER DEFAULT 0"),("hundred_percent","INTEGER DEFAULT 0")])

    def game_already_in_database(self,entry: GameEntry) -> bool:
        """
        Checks if a game entry is already in the database.
        This method will search for an entry with the same name and user in the database.
        :param entry: The GameEntry object to be checked.
        :return: True if the game entry is already in the database, False otherwise.
        """
        query = f"SELECT * FROM {self.table_name} WHERE name = ? AND date = ? AND user = ?"
        data = self.sql_execute_fetchall(query, (entry.name, entry.date, entry.user))
        return len(data) > 0

    def get_game_entry(self,name: str, user: str) -> GameEntry | None:
        """
        Retrieves a game entry from the database based on the name and user.
        :param name: The name of the game.
        :param user: The user who added the game.
        :return: A GameEntry object containing the details of the game.
        """
        query = f"SELECT * FROM {self.table_name} WHERE name = ? AND user = ?"
        data = self.sql_execute_fetchall(query, (name, user))

        print(data)

        if data:
            row = data[0]
            return GameEntry(name=row[0], user=row[1], date=row[2], console=row[3], rating=row[4],review=row[5], replayed=bool(row[7]), hundred_percent=bool(row[8]))

        return None

    def get_all_game_entries_from_user(self, user_name:str) -> list[GameEntry]:
        """
        Retrieves all game entries for a specific user from the database.
        :param user_name: The name of the user whose game entries are to be retrieved.
        :return: A list of GameEntry objects containing the details of all games added by the user.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user = ?"
        data = self.sql_execute_fetchall(query, (user_name,))

        return [GameEntry(name=row[0], user=row[1], date=row[2], console=row[3], rating=row[4], review=row[5], replayed=bool(row[7]), hundred_percent=bool(row[8])) for row in data]

    def get_all_game_entries(self) -> list[GameEntry]:
        """
        Retrieves all game entries from the database.
        :return: A list of all GameEntry objects in the database.
        """
        query = f"SELECT * FROM {self.table_name}"
        data = self.sql_execute_fetchall(query)

        return [GameEntry(name=row[0], user=row[1], date=row[2], console=row[3], rating=row[4], review=row[5], replayed=bool(row[7]), hundred_percent=bool(row[8])) for row in data]

    def put_game(self, entry: GameEntry,old_entry: GameEntry = None):
        """
        If entry is already in the database, it will update the entry.
        Otherwise, it will insert the entry into the database.
        :param entry: The GameEntry object to be added to the database.
        :param old_entry : The old GameEntry object of a game that is being updated.
        If this is None, the entry will be inserted as a new game.
        """
        if old_entry is not None and self.game_already_in_database(old_entry):
            self.remove_entry(old_entry)

        query = f"INSERT INTO {self.table_name} (name, user, date, console, rating, review, replay, hundred_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        params = (entry.name, entry.user, old_entry.date if old_entry else entry.date, entry.console, entry.rating, entry.review, int(entry.replayed), int(entry.hundred_percent))

        self.sql_execute(query, params)

    def remove_entry(self,entry: GameEntry):
        """
        Removes a game entry from the database based on the name, user, and date.
        :param entry: The GameEntry object to be removed from the database.
        """
        query = f"DELETE FROM {self.table_name} WHERE name = ? AND user = ? AND date = ?"
        self.sql_execute(query, (entry.name, entry.user, entry.date))

    def print_database(self):
        """Prints the contents of the database to the console."""
        print("-"*100 + "\nDatabase: " + self._path + "\n" + "-"*100)

        data = self.sql_execute_fetchall("SELECT * FROM games")

        print("Database contains " + str(len(data)) + " entries:")

        for row in data:
            print(" - " + str(row))

        print("-"*100 + "\n")