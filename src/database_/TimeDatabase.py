from common.TimeEntry import TimeEntry
from database_.Database import Database

class TimeDatabase(Database):
    """
    A class to handle database operations for tracking time spent on various activities using SQLite3.
    """
    def __init__(self,folder_path: str):
        super().__init__(folder_path=folder_path,
                         database_name="time_tracking",
                         table_name="time_entries",
                         params=[("user","TEXT"), ("activity","TEXT"),("time_spent","INT")])

    def get_time_entry(self,user: str, activity: str) -> TimeEntry | None:
        """
        Retrieves a time entry for a specific user and activity from the database.
        :param user: The user whose time entry is to be retrieved.
        :param activity: The activity whose time entry is to be retrieved.
        :return: The TimeEntry object if there is one else None
        """
        query = f"SELECT * FROM {self.table_name} WHERE user = ? and activity = ?"
        params = (user,activity)
        data = self.sql_execute_fetchall(query,params)
        if data:
            return TimeEntry(data[0][0],data[0][1],data[0][2])
        return None

    def get_all_time_entries(self,user: str = None) -> list[TimeEntry]:
        """
        Returns all time entries from the database.
        If a user is specified, only returns the time entries for that user.
        :param user: The user whose time entries are to be retrieved. If None, retrieves all entries.
        :return: A list of TimeEntry objects.
        """
        if user is None:
            user_query = "1=1"
        else:
            user_query = f"user = '{user}'"
        query = f"SELECT * FROM {self.table_name} WHERE {user_query}"
        data = self.sql_execute_fetchall(query)

        entries = [TimeEntry(row[0], row[1], row[2]) for row in data]
        return entries

    def put_entry(self,time_entry: TimeEntry):
        """
        Inserts or updates an TimeEntry object in the database.
        If the user of the entry already has an entry for that activity in the database means the entry has to be updated with the new values.
        Else a new entry will be created.
        :param time_entry: The TimeEntry object to be put into the database.
        """
        old_entry = self.get_time_entry(time_entry.user,time_entry.activity)
        if old_entry:
           self.remove_entry(old_entry)

        query = f"INSERT INTO {self.table_name} (user,activity,time_spent) VALUES (?,?,?)"
        params = (time_entry.user,time_entry.activity,time_entry.time_spent)

        self.sql_execute(query,params)

    def remove_entry(self,time_entry: TimeEntry):
        """
        Removes an entry from the database.
        :param time_entry: The TimeEntry object to be removed from the database
        """
        query = f"DELETE FROM {self.table_name} WHERE user = ? AND activity = ?"
        params = (time_entry.user,time_entry.activity)
        self.sql_execute(query,params)

    def get_users(self) -> list[str]:
        """
        Retrieves a list of all users who have time entries in the database.
        :return: A list of usernames.
        """
        query = f"SELECT DISTINCT user FROM {self.table_name}"
        data = self.sql_execute_fetchall(query)

        return [row[0] for row in data]

    def print_database(self):
        """Prints the contents of the time tracking database to the console."""
        print("-" * 100 + "\nDatabase: " + self._path + "\n" + "-" * 100)

        entries = self.get_all_time_entries()
        for entry in entries:
            print(entry)

        print("-" * 100 + "\n")