import sqlite3

from common.TimeUtils import TimeUtils

class Database:
    def __init__(self, folder_path: str,database_name: str, params: list[tuple]):
        self.__path = folder_path + database_name + TimeUtils.get_current_year_formated() + ".db"
        self.__init_database(params)
        self.print_database()

    def sql_execute(self,query: str, params: tuple = ()):
        connection = sqlite3.connect(self.__path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()

    def sql_execute_fetchall(self, query: str, params: tuple = ()) -> list:
        connection = sqlite3.connect(self.__path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()

        return data

    def __init_database(self,params: list[tuple]):
        paramList = []
        for param in params:
            paramList.append(f"{param[0]} {param[1]}")

        create_table_command = 'CREATE TABLE IF NOT EXISTS games (' + ', '.join(paramList) + ')'

        self.sql_execute(create_table_command)

    def print_database(self):
        print("-"*100 + "\nDatabase: " + self.__path + "\n" + "-"*100)

        data = self.sql_execute_fetchall("SELECT * FROM games")

        print("Database contains " + str(len(data)) + " entries:\n")

        for row in data:
            print(" - " + str(row))

        print("-"*100 + "\n")