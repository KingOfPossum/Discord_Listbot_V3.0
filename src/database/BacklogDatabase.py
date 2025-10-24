from common.BacklogEntry import BacklogEntry
from database.Database import Database

class BacklogDatabase(Database):
    """
    A database to manage backlog items.
    """
    def __init__(self,folder_path: str):
        super().__init__(folder_path=folder_path,
                         database_name="backlog",
                         table_name="backlog_items",
                         params=[("name","TEXT"),("user","TEXT"),("recommended_by","TEXT")])

    def add_entry(self,entry:BacklogEntry):
        """
        Adds a backlog entry to the database.
        :param entry: The backlog entry to add.
        """
        query = f"INSERT INTO {self.table_name} (name,user,recommended_by) Values (?,?,?)"
        data = (entry.name,entry.user,entry.recommended_by)
        self.sql_execute(query,data)

    def remove_entry(self,entry:BacklogEntry):
        """
        Removes a backlog entry from the database.
        :param entry: The backlog entry to remove.
        """
        query = f"DELETE FROM {self.table_name} WHERE name=? AND user=?"
        data = (entry.name,entry.user)
        self.sql_execute(query,data)

    def get_entry(self,name:str, user:str) -> BacklogEntry|None:
        """
        Retrieves a backlog entry from the database.
        :param name: The name of the game.
        :param user: The user who has this game in their backlog.
        :return: The backlog entry if found, otherwise None.
        """
        query = f"SELECT * FROM {self.table_name} WHERE name=? AND user=?"
        data = (name,user)
        result = self.sql_execute_fetchall(query,data)
        if not result:
            return None
        else:
            row = result[0]
            return BacklogEntry(row[0],row[1],row[2])

    def get_all_entries(self,user: str = None) -> list[BacklogEntry]:
        """
        Retrieves all backlog entries for a specific user.
        :param user: The user whose backlog entries to retrieve.
        :return: A list of backlog entries.
        """
        if user is None:
            user_txt = "1=1"
        else:
            user_txt = f"user='{user}'"
        query = f"SELECT * FROM {self.table_name} WHERE {user_txt}"
        result = self.sql_execute_fetchall(query)
        if not result:
            return list()
        else:
            return [BacklogEntry(row[0],row[1],row[2]) for row in result]

    def users_with_backlog(self) -> list[str]:
        """
        Retrieves a list of users who have backlog entries.
        :return: A list of usernames.
        """
        query = f"SELECT DISTINCT user FROM {self.table_name}"
        result = self.sql_execute_fetchall(query)
        if not result:
            return list()
        else:
            return [row[0] for row in result]

    def print_database(self):
        """
        Prints the entire backlog database to the console.
        """
        entries = self.get_all_entries()
        print("-"*100 + "\nDatabase: " + self._path + "\n" + "-"*100)
        entry_txt_list = list()
        for entry in entries:
            entry_txt_list.append(f"- Name: {entry.name} | User: {entry.user} | Recommended By: {entry.recommended_by}")
        print("\n".join(entry_txt_list))
        print("-" * 100 + "\n")