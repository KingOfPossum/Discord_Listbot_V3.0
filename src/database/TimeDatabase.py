from database.Database import Database

class TimeDatabase(Database):
    """
    A class to handle database operations for tracking time spent on various activities using SQLite3.
    """
    def __init__(self,folder_path: str):
        super().__init__(folder_path=folder_path,
                         database_name="time_tracking",
                         table_name="time_entries",
                         params=[("user","TEXT"), ("activity","TEXT"),("time_spent","INT")])

    def get_all_time_entries(self,user: str = None) -> dict:
        """
        Returns all time entries from the database.
        If a user is specified, only returns the time entries for that user.
        :param user: The user whose time entries are to be retrieved. If None, retrieves all entries.
        :return: A dictionary where the keys are usernames and the values are lists of tuples (activity, time_spent).
        """

        if user is None:
            user_query = "1=1"
        else:
            user_query = f"user = '{user}'"
        query = f"SELECT * FROM {self.table_name} WHERE {user_query}"
        data = self.sql_execute_fetchall(query)

        users = {row[0] for row in data}

        result = {}
        for user in users:
            result[user] = list()

        for row in data:
            result[row[0]].append((row[1], row[2]))

        return result

    def put_entry(self,user: str, activity: str, time_spent: int,is_new:bool = True):
        """
        If an entry for the same user and activity already exists, it will update the time spent by adding the new time to the existing time.
        Else it will create a new entry in the database.
        :param user: The user of the activity.
        :param activity: The name of the activity.
        :param time_spent: The time spent on the activity in seconds.
        :param is_new: Whether the entry is new or not.
        """
        if not is_new:
           self.remove_entry(user,activity)

        query = f"INSERT INTO {self.table_name} (user,activity,time_spent) VALUES (?,?,?)"
        params = (user,activity,time_spent)

        self.sql_execute(query,params)

    def remove_entry(self,user:str, activity:str):
        """
        Removes an entry from the database.
        :param user: The user of the activity.
        :param activity: The name of the activity.
        """
        query = f"DELETE FROM {self.table_name} WHERE user = ? AND activity = ?"
        params = (user,activity)
        self.sql_execute(query,params)

    def print_database(self):
        """Prints the contents of the time tracking database to the console."""
        print("-" * 100 + "\nDatabase: " + self._path + "\n" + "-" * 100)

        entries = self.get_all_time_entries()
        for user in entries.keys():
            print(f"User: {user}")
            for activity, time_spent in entries[user]:
                print(f" - Activity: {activity}, Time Spent: {time_spent} seconds")

        print("-" * 100 + "\n")