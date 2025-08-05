import sqlite3

from common.GameEntry import GameEntry
from common.TimeUtils import TimeUtils

class Database:
    """A class to handle database operations using SQLite3."""

    def __init__(self, folder_path: str,database_name: str,table_name: str, params: list[tuple]):
        """
        Initializes the database with the specified folder path, database name, and parameters.
        It will set the path for the database by concatenating the folder path, database name, and the current year.
        :param folder_path: Path to the databases' folder.
        :param database_name: The name of the database to be created.
        :param params: A list of tuples where each tuple contains the column name and its data type for the database table.
        """
        self.table_name = table_name
        self.__path = folder_path + database_name + TimeUtils.get_current_year_formated() + ".db"
        self.__init_database(table_name,params)
        self.print_database()

    def sql_execute(self,query: str, params: tuple = ()):
        """
        Executes a SQL command on the database.
        This method is used for commands that do not return data, such as INSERT, UPDATE, or DELETE.
        It will connect to the database, execute the query with the provided parameters, and commit the changes.
        :param query: The SQL query to be executed.
        :param params: The parameters to be used in the SQL query. Default is an empty tuple.
        """
        connection = sqlite3.connect(self.__path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()

    def sql_execute_fetchall(self, query: str, params: tuple = ()) -> list:
        """
        Executes a SQL command on the database and fetches all results.
        This method is used for commands that return data, such as SELECT.
        It will connect to the database, execute the query with the provided parameters, and return all results.
        :param query: The SQL query to be executed.
        :param params: The parameters to be used in the SQL query. Default is an empty tuple.
        :return: The data fetched from the database as a list of tuples.
        """
        connection = sqlite3.connect(self.__path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()

        return data

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

    def put_game(self, entry: GameEntry):
        """
        If entry is already in the database, it will update the entry.
        Otherwise, it will insert the entry into the database.
        :param entry: The GameEntry object to be added to the database.
        """
        if self.game_already_in_database(entry):
            query = f"UPDATE {self.table_name} SET console = ?, rating = ?, genre = ?, review = ?, replay = ?, hundred_percent = ? WHERE name = ? AND date = ? AND user = ?"
            params = (entry.console, entry.rating, entry.genre, entry.review, int(entry.replayed), int(entry.hundred_percent),entry.name, entry.date, entry.user)

        else:
            query = f"INSERT INTO {self.table_name} (name, user, date, console, rating, genre, review, replay, hundred_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (entry.name, entry.user, entry.date, entry.console, entry.rating, entry.genre, entry.review, int(entry.replayed), int(entry.hundred_percent))

        self.sql_execute(query, params)

    def get_game_entry(self,name: str, user: str, date: str) -> GameEntry:
        """
        Retrieves a game entry from the database based on the name, user, and date.
        :param name: The name of the game.
        :param user: The user who added the game.
        :param date: The date when the game was added.
        :return: A GameEntry object containing the details of the game.
        """
        query = f"SELECT * FROM {self.table_name} WHERE name = ? AND user = ? AND date = ?"
        data = self.sql_execute_fetchall(query, (name, user, date))

        if data:
            row = data[0]
            return GameEntry(name=row[0], user=row[1], date=row[2], console=row[3], rating=row[4], genre=row[5], review=row[6], replayed=bool(row[7]), hundred_percent=bool(row[8]))

        return None

    def __init_database(self,table_name: str,params: list[tuple]):
        """
        Initializes the database by creating a table with the specified name and parameters if it does not already exist.
        The parameters should be a list of tuples where each tuple contains the column name and its data type.
        :param table_name: The name of the table to be created.
        :param params: The parameter for the table to be created, in the format [(column_name, data_type), ...].
        """
        print("Initializing database at: " + self.__path)

        paramList = []
        for param in params:
            paramList.append(f"{param[0]} {param[1]}")

        create_table_command = f'CREATE TABLE IF NOT EXISTS {table_name} (' + ', '.join(paramList) + ')'

        self.sql_execute(create_table_command)

    def print_database(self):
        """Prints the contents of the database to the console."""
        print("-"*100 + "\nDatabase: " + self.__path + "\n" + "-"*100)

        data = self.sql_execute_fetchall("SELECT * FROM games")

        print("Database contains " + str(len(data)) + " entries:\n")

        for row in data:
            print(" - " + str(row))

        print("-"*100 + "\n")