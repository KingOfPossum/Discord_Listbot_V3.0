from common.BacklogEntry import BacklogEntry
from dataclasses import astuple
from database.Database import Database

class BacklogDatabase(Database):
    """
    A database to manage backlog items.
    """
    def __init__(self,folder_path: str):
        schema = """
        game_name TEXT NOT NULL,
        user_id INTEGER,
        recommended_by_user INTEGER,
        PRIMARY KEY (game_name,user_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (recommended_by_user) REFERENCES users(user_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="backlog",
                         schema=schema)

    def add_entry(self,entry:BacklogEntry):
        """
        Adds a backlog entry to the database.
        :param entry: The backlog entry to add.
        """
        query = f"INSERT INTO {self.table_name} (game_name,user_id,recommended_by_user) Values (?,?,?)"
        data = (astuple(entry))
        self.sql_execute(query,data)

    def remove_entry(self,entry:BacklogEntry):
        """
        Removes a backlog entry from the database.
        :param entry: The backlog entry to remove.
        """
        query = f"DELETE FROM {self.table_name} WHERE game_name=? AND user_id=?"
        data = (entry.game_name,entry.user_id)
        self.sql_execute(query,data)

    def get_entry(self,game_name:str, user_id:int) -> BacklogEntry|None:
        """
        Retrieves a backlog entry from the database.
        :param game_name: The name of the game.
        :param user_id: The ID of the user who has this game in his backlog.
        :return: The backlog entry if found, otherwise None.
        """
        query = f"SELECT * FROM {self.table_name} WHERE game_name=? AND user_id=?"
        data = (game_name,user_id)
        result = self.sql_execute_fetchall(query,data)

        return BacklogEntry(*result[0]) if result else None

    def get_all_entries(self,user_id: int = None) -> list[BacklogEntry]:
        """
        Retrieves all backlog entries for a specific user if a user is provided else retrieves all entries for all users.
        :param user_id: The ID of the user whose backlog entries to retrieve.
        :return: A list of backlog entries.
        """
        user_txt = f"user_id='{user_id}'" if user_id else "1=1"
        query = f"SELECT * FROM {self.table_name} WHERE {user_txt}"
        result = self.sql_execute_fetchall(query)

        return [BacklogEntry(*row) for row in result] if result else list()

    def get_users(self) -> list[int]:
        """
        Retrieves a list of users who have backlog entries.
        :return: A list of user_ids.
        """
        query = f"SELECT DISTINCT user_id FROM {self.table_name}"
        result = self.sql_execute_fetchall(query)

        return [row[0] for row in result] if result else list()

    def print_database(self):
        """
        Prints the entire backlog database to the console.
        """
        entries = self.get_all_entries()
        print("-"*100 + "\nDatabase: " + self._path + "\n" + "-"*100)
        for entry in entries:
            print(entry)
        print("-" * 100 + "\n")