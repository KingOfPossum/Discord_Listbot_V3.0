from dataclasses import astuple

import discord

from common.MessageManager import MessageManager
from common.TokensEntry import TokensEntry
from common.UserManager import UserManager
from database.Database import Database

class TokensDatabase(Database):
    """
    A class to handle database operations concerning the tokens system using SQLite3.
    """
    def __init__(self,folder_path: str):
        schema = """
        user_id INTEGER,
        tokens INTEGER DEFAULT 0,
        coins INTEGER DEFAULT 0,
        needed_tokens INTEGER DEFAULT 3,
        PRIMARY KEY (user_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        """

        super().__init__(folder_path=folder_path,
                         table_name="tokens",
                         schema=schema)

    def get_tokens_entry(self,user_id: int, add_default=True) -> TokensEntry | None:
        """
        Retrieves the TokensEntry for a specific user from the database.
        :param user_id: The ID of the user TokensEntry is to be retrieved.
        :param add_default: If True, add an empty entry if the user does not exist in the database.
        :return: The TokensEntry object for the user.
        """
        query = f"SELECT * FROM {self.table_name} WHERE user_id = ?"
        params = (user_id,)

        data = self.sql_execute_fetchall(query,params)

        if data:
            entry = TokensEntry(*data[0])
            return entry

        if add_default:
            empty_entry = TokensEntry(user_id=user_id,tokens=0,coins=0,needed_tokens=3)
            self.put_tokens_entry(empty_entry)
            return empty_entry
        return None

    def get_all_tokens_entries(self) -> list[TokensEntry]:
        """"
        Retrieves all TokensEntry objects from the database.
        :return: A list containing all TokensEntry objects
        """
        users = UserManager.accepted_users
        return [self.get_tokens_entry(user.id) for user in users]

    def put_tokens_entry(self, entry: TokensEntry):
        """
        Inserts or updates a TokensEntry in the database.
        :param entry: The TokensEntry object to be put into the database.
        """
        query = f"""
                INSERT INTO {self.table_name} (user_id, tokens, coins, needed_tokens)
                VALUES (?,?,?,?)
                ON CONFLICT(user_id)
                DO UPDATE SET
                tokens = excluded.tokens,
                coins = excluded.coins,
                needed_tokens = excluded.needed_tokens
                """
        self.sql_execute(query, astuple(entry))

    async def add_token(self,user_id:int,ctx:discord.interactions = None,interaction: discord.Interaction = None):
        """
        Adds a token to the specified user in the database.
        If the user reaches the required number of tokens, they will be awarded a coin.
        :param user_id: The user to whom the token will be added.
        :param ctx: The interactions context
        """
        entry = self.get_tokens_entry(user_id)
        entry.tokens += 1
        if entry.tokens % entry.needed_tokens == 0:
            entry.coins += 1

            user_entry = UserManager.get_user_entry(user_id=user_id)
            await MessageManager.send_message(ctx.channel if ctx else interaction.channel,f"Congratulations {user_entry.display_name}, you have earned a coin! You now have {entry.coins} coins.")

        self.put_tokens_entry(entry)

    def remove_coin(self,user_id:int) -> TokensEntry | None:
        """
        Removes a coin from the specified user in the database.
        :param user_id: The ID of the user from whom the coin will be removed.
        :return: The TokensEntry with updated coin value if the user had a coin else None.
        """
        entry = self.get_tokens_entry(user_id)
        if entry.coins > 0:
            entry.coins -= 1
            self.put_tokens_entry(entry)
            return entry

        return None

    def remove_entry(self, entry: TokensEntry):
        """
        Removes an entry from the tokens' database.
        :param entry: The TokensEntry object to be removed from the database.
        """
        query = f"DELETE FROM {self.table_name} WHERE user_id = ?"
        params = (entry.user_id,)
        self.sql_execute(query, params)

    def set_needed_tokens(self,user_id:int, needed_tokens:int):
        """
        Set the number of tokens needed to earn a coin for a specific user.
        :param user_id: The ID of the user for whom to set the needed tokens.
        :param needed_tokens: The new amount of tokens needed to earn a coin.
        """
        entry = self.get_tokens_entry(user_id)
        entry.needed_tokens = needed_tokens
        self.put_tokens_entry(entry)

    def print_database(self):
        """
        Prints the entire tokens database to the console.
        This method retrieves all entries from the tokens database and prints them in a readable format.
        """
        print("-"*100 + "\nDatabase: " + self._path + "\n" + "-"*100)
        entries = self.get_all_tokens_entries()
        for entry in entries:
            print(f"UserID: {entry.user_id} | Tokens: {entry.tokens} | Coins: {entry.coins} | Needed Tokens: {entry.needed_tokens}")
        print("-" * 100 + "\n")