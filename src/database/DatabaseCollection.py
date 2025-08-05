import os
from database.Database import Database

class DatabaseCollection:
    """
    A collection of databases.
    """

    def __init__(self,database_folder_path: str):
        """
        Initializes the DatabaseCollection with a specified folder path where the databases should be created.
        If the folder does not exist, it will be created.
        Will also initialize the databases used. (Currently only the list database is initialized.)
        :param database_folder_path: The path to the folder where the databases will be stored.
        """
        self.create_database_folder_if_not_exists(database_folder_path)

        self.__database_folder_path = database_folder_path
        self.listDatabase: Database = Database(self.__database_folder_path,"list","games",[("name","TEXT"), ("user","TEXT"),("date","DATE"),("console","TEXT"),("rating","INT"),("genre","TEXT"),("review","TEXT"),("cover","TEXT"),("replay","INTEGER DEFAULT 0"),("hundred_percent","INTEGER DEFAULT 0")])

    @staticmethod
    def create_database_folder_if_not_exists(database_folder_path: str):
        """
        Creates the database folder if it does not exist.
        This is necessary to ensure that the databases can be created in the specified folder otherwise it would throw an error.
        :param database_folder_path: Path to the folder where the databases should be created.
        """
        if not os.path.exists(database_folder_path):
            print("Creating database folder at: " + database_folder_path)
            os.makedirs(database_folder_path)