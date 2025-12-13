import Database

from common.UserEntry import UserEntry

class UserDatabase(Database):
    """
    Database table for storing user information.
    """
    def __init__(self,folder_path: str):
        super().__init__(folder_path=folder_path,
                         table_name="Users",
                         params=["user_id INTEGER NOT NULL", "user_name TEXT NOT NULL","display_name TEXT","PRIMARY KEY(user_id)"])

    def add_entry(self,entry: UserEntry):
        """
        Adds a new user entry to the database.
        :param entry: The UserEntry object containing the user's information.
        """
        query = f"INSERT OR REPLACE INTO {self.table_name} (user_id,user_name,display_name) VALUES (?,?,?)"
        params = (entry.user_id, entry.user_name, entry.display_name)

        self.sql_execute(query, params)

    def get_user_by_id(self,user_id: int) -> UserEntry | None:
        """
        Retrieves a user from the database based on the unique user ID.
        :param user_id: The user ID of the user to be retrieved.
        :return: The UserEntry object containing the user's information.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user_id = {user_id}"
        data = self.sql_execute_fetchall(query)

        if not data:
            return None

        return UserEntry(*data)

    def get_all_users(self) -> list[UserEntry]:
        """
        Retrieves all users from the database.
        :return: A list of UserEntry objects containing all users' information.
        """
        query = f"SELECT * FROM {self.table_name}"
        data = self.sql_execute_fetchall(query)

        return [UserEntry(*row) for row in data]

    def print_database(self):
        """
        Prints the contents of the Users database table.
        """
        print(100 * "-" + f"\nDatabase: {self.table_name}\n" + 100 * "-")

        user_entries = self.get_all_users()
        for entry in user_entries:
            print(entry)

        print(100 * "-" + "\n")