import sqlite3

from abc import abstractmethod

class Database:
    """
    A class to handle basic database operations using SQLite3.
    """
    def __init__(self,folder_path: str,table_name: str,params: list[str]):
        """
        Initializes the Database by creating the corresponding table if it doesn't exist already.
        :param folder_path: The path to the folder where the database file is located.
        :param table_name: The name of the table to be created/used in the database.
        :param params: The list of parameters defining the table schema.
        """
        self.table_name = table_name
        self._path = folder_path + "/database.db"

        self._init_databases(params)
        self.print_database()

    def _init_databases(self,params: list[str]):
        """
        Creates the database table if it does not already exist.
        Takes a list of parameters to define the table schema. With each parameter defining a column name and its features.
        :param params: A list of strings defining the table schema.
        :return:
        """
        print(f"Initializing database : {self.table_name}")

        create_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({', '.join(params)})"
        self.sql_execute(create_query)

    def sql_execute(self, query: str, params: tuple = ()):
        """
        Executes a SQL command on the database.
        This method is used for commands that do not return data, such as INSERT, UPDATE, or DELETE.
        It will connect to the database, execute the query with the provided parameters, and commit the changes.
        :param query: The SQL query to be executed.
        :param params: The parameters to be used in the SQL query. Default is an empty tuple.
        """
        connection = sqlite3.connect(self._path)
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
        connection = sqlite3.connect(self._path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()

        return data

    @abstractmethod
    def print_database(self):
        """
        Prints the contents of the database in a readable format.
        """
        pass