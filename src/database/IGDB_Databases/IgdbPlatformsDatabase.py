from database.Database import Database

class IGDBPlatformsDatabase(Database):
    def __init__(self,folder_path: str):
        schema = """
        platform_id INTEGER,
        platform_name TEXT NOT NULL,
        PRIMARY KEY (platform_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="igdb_platforms",
                         schema=schema)

    def add_platform(self, platform_name: str) -> int:
        """
        Adds a platform to the database and returns the created platform_id.
        :param platform_name: The name of the platform to be added to the database.
        :returns: The platform_id of the newly added platform.
        """
        query = f"INSERT INTO {self.table_name} (platform_name) VALUES (?)"
        self.sql_execute(query, (platform_name,))

        query = f"SELECT platform_id FROM {self.table_name} WHERE platform_name = ?"
        result = self.sql_execute_fetchall(query, (platform_name,))
        return result[0][0] if result else None

    def platform_exists(self, platform_name: str) -> int | None:
        """
        Checks if a platform with the given platform_name already exists in the database.
        If the platform exists, returns the platform_id. Otherwise, returns None.
        :param platform_name: The name of the platform to check for existence.
        :return: The platform_id of the platform if it exists in the database, None otherwise.
        """
        query = f"SELECT platform_id FROM {self.table_name} WHERE platform_name = ?"
        result = self.sql_execute_fetchall(query, (platform_name,))

        if len(result) == 0:
            return None

        return result[0][0]

    def print_database(self):
        pass