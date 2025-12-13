import sqlite3

from abc import abstractmethod
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
        self._path = folder_path + database_name + ".db"
        self._init_database(table_name,params)
        self.print_database()

    def _init_database(self,table_name: str,params: list[tuple]):
        """
        Initializes the database by creating a table with the specified name and parameters if it does not already exist.
        The parameters should be a list of tuples where each tuple contains the column name and its data type.
        :param table_name: The name of the table to be created.
        :param params: The parameter for the table to be created, in the format [(column_name, data_type), ...].
        """
        print("Initializing database at: " + self._path)

        paramList = []
        for param in params:
            paramList.append(f"{param[0]} {param[1]}")

        create_table_command = f'CREATE TABLE IF NOT EXISTS {table_name} (' + ', '.join(paramList) + ')'

        self.sql_execute(create_table_command)

    def sql_execute(self,query: str, params: tuple = ()):
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
        pass