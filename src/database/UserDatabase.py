from common.UserEntry import UserEntry
from database.Database import Database

class UserDatabase(Database):
    """
    Database class to handle user-related operations using SQLite3.
    """
    def __init__(self,folder_path: str):
        schema = """
        user_id INTEGER,
        user_name TEXT NOT NULL,
        display_name TEXT,
        PRIMARY KEY (user_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="users",
                         schema=schema)

    def get_all_users(self) -> list[UserEntry]:
        """
        Returns all UserEntry objects in the user database.
        :return: list of UserEntry objects
        """
        data = self.sql_execute_fetchall(f'SELECT * FROM {self.table_name}')
        return [UserEntry(*row) for row in data]

    def get_user_by_id(self,user_id: int) -> UserEntry | None:
        """
        Retrieves a UserEntry from the database based on the unique user ID.
        :param user_id: The unique ID of the user.
        :return: The UserEntry object containing the details of the user, or None if not found.
        """
        data = self.sql_execute_fetchall(f'SELECT * FROM {self.table_name} WHERE user_id = {user_id}')
        if not data:
            return None

        return UserEntry(*data[0])

    def user_exists(self,user_id: int) -> bool:
        """
        Checks if a user exists in the database based on the unique user ID.
        :param user_id: The unique ID of the user.
        :return: True if the user exists, False otherwise.
        """
        data = self.sql_execute_fetchall(f'SELECT * FROM {self.table_name} WHERE user_id = {user_id}')
        return len(data) == 1

    def add_user(self,user: UserEntry):
        """
        Adds a new user to the database if they do not already exist.
        If the user already exists, updates their information.
        :param user: The UserEntry object containing the details of the user to be added.
        """
        query = f"""
        INSERT INTO {self.table_name} (user_id, user_name, display_name)
        VALUES ({user.user_id}, {user.user_name}, {user.display_name})
        ON CONFLICT (user_id)
        DO UPDATE SET
            user_name = excluded.user_name,
            display_name = excluded.display_name
        """

        self.sql_execute(query)

    def print_database(self):
        """
        Prints all entries in the user database.
        """
        user_entries = self.get_all_users()
        for user in user_entries:
            print(user)