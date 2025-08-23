import discord

from common.TokensEntry import TokensEntry
from common.UserManager import UserManager
from database.Database import Database

class TokensDatabase(Database):
    """
    A class to handle database operations concerning the tokens system using SQLite3.
    """
    def __init__(self,folder_path: str):
        super().__init__(folder_path=folder_path,
                         database_name="tokens",
                         table_name="tokens",
                         params=[("user","TEXT"), ("tokens","INT DEFAULT 0"),("coins","INT DEFAULT 0"),("needed_tokens","INT DEFAULT 3")])

    def get_tokens_entry(self,user: str, add_default=True) -> TokensEntry | None:
        """
        Retrieves the TokensEntry for a specific user from the database.
        :param user: The user whose TokensEntry is to be retrieved.
        :param add_default: If True, add an empty entry if the user does not exist in the database.
        :return: The TokensEntry object for the user.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user = ?"
        params = (user,)

        data = self.sql_execute_fetchall(query,params)

        if data:
            row = data[0]
            entry = TokensEntry(user=row[0], tokens=row[1], coins=row[2], needed_tokens=row[3])
            return entry

        if add_default:
            empty_entry = TokensEntry(user=user,tokens=0,coins=0,needed_tokens=3)
            self.put_tokens_entry(empty_entry)
            return empty_entry
        return None

    def get_all_tokens_entries(self) -> list[TokensEntry]:
        """"
        Retrieves all TokensEntry objects from the database.
        :return: A list containing all TokensEntry objects
        """
        users = UserManager.accepted_users
        return [self.get_tokens_entry(user) for user in users]

    def put_tokens_entry(self, entry: TokensEntry):
        """
        Inserts or updates a TokensEntry in the database.
        If the user of the entry already has an entry in the database means the entry has to be updated with the new values.
        The update will happen by deleting the old entry and inserting the new one.
        :param entry: The TokensEntry object to be put into the database.
        """
        old_entry = self.get_tokens_entry(entry.user, add_default=False)
        if old_entry:
            self.remove_entry(old_entry)
        query = f"INSERT INTO {self.table_name} (user, tokens, coins, needed_tokens) VALUES (?,?,?,?)"
        params = (entry.user, entry.tokens, entry.coins, entry.needed_tokens)
        self.sql_execute(query, params)

    async def add_token(self,user:str,ctx:discord.interactions = None):
        """
        Adds a token to the specified user in the database.
        If the user reaches the required number of tokens, they will be awarded a coin.
        :param user: The user to whom the token will be added.
        :param ctx: The interactions context
        """
        entry = self.get_tokens_entry(user)
        entry.tokens += 1
        if entry.tokens % entry.needed_tokens == 0:
            entry.coins += 1
            if ctx:
                await ctx.send(f"Congratulations {user}, you have earned a coin! You now have {entry.coins} coins.")

        self.put_tokens_entry(entry)

    def remove_coin(self,user:str) -> TokensEntry | None:
        """
        Removes a coin from the specified user in the database.
        :param user: The user from whom the coin will be removed.
        :return: The TokensEntry with updated coin value if the user had a coin else None.
        """
        entry = self.get_tokens_entry(user)
        if entry.coins > 0:
            entry.coins -= 1
            self.put_tokens_entry(entry)
            return entry
        return None

    def remove_entry(self, entry: TokensEntry):
        """
        Removes an entry from the tokens database.
        :param entry: The TokensEntry object to be removed from the database.
        """
        query = f"DELETE FROM {self.table_name} WHERE user = ?"
        params = (entry.user,)
        self.sql_execute(query, params)

    def print_database(self):
        """
        Prints the entire tokens database to the console.
        This method retrieves all entries from the tokens database and prints them in a readable format.
        """
        print("-"*100 + "\nDatabase: " + self._path + "\n" + "-"*100)
        entries = self.get_all_tokens_entries()
        for entry in entries:
            print(f"User: {entry.user} | Tokens: {entry.tokens} | Coins: {entry.coins} | Needed Tokens: {entry.needed_tokens}")
        print("-" * 100 + "\n")