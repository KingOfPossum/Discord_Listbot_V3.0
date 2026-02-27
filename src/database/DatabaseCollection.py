import os

from database.BacklogDatabase import BacklogDatabase
from database.IGDB_Databases.IgdbDatabaseCollection import IGDBDatabaseCollection
from database.ListDatabase import ListDatabase
from database.TimeDatabase import TimeDatabase
from database.TokensDatabase import TokensDatabase
from database.UserDatabase import UserDatabase

class DatabaseCollection:
    """
    A collection of databases.
    """
    igdb_databases: IGDBDatabaseCollection = None
    user_database: UserDatabase = None
    list_database: ListDatabase = None
    tokens_database: TokensDatabase = None
    time_database: TimeDatabase = None
    backlog_database: BacklogDatabase = None

    def __init__(self,database_folder_path: str):
        """
        Initializes the DatabaseCollection with a specified folder path where the databases should be created.
        If the folder does not exist, it will be created.
        Will also initialize the databases used. (Currently only the list database is initialized.)
        :param database_folder_path: The path to the folder where the databases will be stored.
        """
        self.create_database_folder_if_not_exists(database_folder_path)
        self.__database_folder_path = database_folder_path

    def init_databases(self):
        """
        Initializes all databases.
        """
        DatabaseCollection.user_database = UserDatabase(self.__database_folder_path)
        DatabaseCollection.list_database = ListDatabase(self.__database_folder_path)
        DatabaseCollection.tokens_database = TokensDatabase(self.__database_folder_path)
        DatabaseCollection.time_database = TimeDatabase(self.__database_folder_path)
        DatabaseCollection.backlog_database = BacklogDatabase(self.__database_folder_path)
        DatabaseCollection.igdb_databases = IGDBDatabaseCollection(self.__database_folder_path)

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