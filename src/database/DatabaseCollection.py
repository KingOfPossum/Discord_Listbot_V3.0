import os

from database.BacklogDatabase import BacklogDatabase
from database.ListDatabase import ListDatabase
from database.TimeDatabase import TimeDatabase
from database.TokensDatabase import TokensDatabase
from database.UserDatabase import UserDatabase

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

        self.user_database: UserDatabase = None
        self.list_database: ListDatabase = None
        self.tokens_database: TokensDatabase = None
        self.time_database: TimeDatabase = None
        self.backlog_database: BacklogDatabase = None

    def init_user_database(self):
        """
        Initializes the user database.
        """
        self.user_database: UserDatabase = UserDatabase(self.__database_folder_path)

    def init_list_database(self):
        """
        Initializes the list database.
        """
        self.list_database: ListDatabase = ListDatabase(self.__database_folder_path)

    def init_tokens_database(self):
        """
        Initializes the tokens database.
        """
        self.tokens_database: TokensDatabase = TokensDatabase(self.__database_folder_path)

    def init_time_database(self):
        """
        Initializes the time tracking database.
        """
        self.time_database: TimeDatabase = TimeDatabase(self.__database_folder_path)

    def init_backlog_database(self):
        """
        Initializes the backlog database.
        """
        self.backlog_database: BacklogDatabase = BacklogDatabase(self.__database_folder_path)

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