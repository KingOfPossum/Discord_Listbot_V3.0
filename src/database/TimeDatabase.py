from common.TimeEntry import TimeEntry
from database.Database import Database
from dataclasses import astuple

class TimeDatabase(Database):
    """
    A class to handle database operations for tracking time spent on various activities using SQLite3.
    """
    def __init__(self,folder_path: str):
        schema = """
        user_id INTEGER,
        activity TEXT NOT NULL,
        time_spent INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, activity),
        FOREIGN KEY (user_id) REFERENCES users(id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="timetracking",
                         schema=schema)

    def get_time_entry(self,user_id: int, activity: str) -> TimeEntry | None:
        """
        Retrieves a time entry for a specific user and activity from the database.
        :param user_id: The ID of the user whose time entry is to be retrieved.
        :param activity: The activity whose time entry is to be retrieved.
        :return: The TimeEntry object if there is one else None
        """
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ? and activity = ?"
        params = (user_id,activity)
        data = self.sql_execute_fetchall(query,params)
        if data:
            return TimeEntry(*data[0])
        return None

    def get_all_time_entries(self,user_id: int = None) -> list[TimeEntry]:
        """
        Returns all time entries from the database.
        If a user is specified, only returns the time entries for that user.
        :param user_id: The ID of the user whose time entries are to be retrieved. If None, retrieves all entries.
        :return: A list of TimeEntry objects.
        """
        if user_id is None:
            user_query = "1=1"
        else:
            user_query = f"user_id = '{user_id}'"
        query = f"SELECT * FROM {self.table_name} WHERE {user_query}"
        data = self.sql_execute_fetchall(query)

        entries = [TimeEntry(*row) for row in data]
        return entries

    def put_entry(self,time_entry: TimeEntry):
        """
        Inserts or updates an TimeEntry object in the database.
        :param time_entry: The TimeEntry object to be put into the database.
        """
        query = f"""
                INSERT INTO {self.table_name}
                VALUES(?,?,?)
                ON CONFLICT(user_id,activity)
                DO UPDATE SET
                time_spent = excluded.time_spent
                """

        self.sql_execute(query,astuple(time_entry))

    def remove_entry(self,time_entry: TimeEntry):
        """
        Removes an entry from the database.
        :param time_entry: The TimeEntry object to be removed from the database
        """
        query = f"DELETE FROM {self.table_name} WHERE user_id = ? AND activity = ?"
        params = (time_entry.user_id,time_entry.activity)
        self.sql_execute(query,params)

    def get_users(self) -> list[int]:
        """
        Retrieves a list of all users who have time entries in the database.
        :return: A list of all user_ids.
        """
        query = f"SELECT DISTINCT user_id FROM {self.table_name}"
        data = self.sql_execute_fetchall(query)

        return [row[0] for row in data]

    def print_database(self):
        """Prints the contents of the time tracking database to the console."""
        print("-" * 100 + "\nDatabase: " + self._path + "\n" + "-" * 100)

        entries = self.get_all_time_entries()
        for entry in entries:
            print(entry)

        print("-" * 100 + "\n")