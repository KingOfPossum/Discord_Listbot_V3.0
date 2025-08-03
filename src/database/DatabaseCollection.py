import os
from database.Database import Database

class DatabaseCollection:
    database_folder_path = ""
    listDatabase: Database = None

    def __init__(self,database_folder_path: str):
        self.database_folder_path = database_folder_path
        self.listDatabase: Database = Database(self.database_folder_path,"list",[("name","TEXT"), ("user","TEXT"),("date","DATE"),("console","TEXT"),("rating","INT"),("genre","TEXT"),("review","TEXT"),("cover","TEXT"),("replay","INTEGER DEFAULT 0"),("hundred_percent","INTEGER DEFAULT 0")])

    @staticmethod
    def create_database_folder_if_not_exists(database_folder_path: str):
        if not os.path.exists(database_folder_path):
            os.makedirs(database_folder_path)