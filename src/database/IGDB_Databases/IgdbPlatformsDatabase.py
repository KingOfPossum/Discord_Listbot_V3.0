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

    def print_database(self):
        pass