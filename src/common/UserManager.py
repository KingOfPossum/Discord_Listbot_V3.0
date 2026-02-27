from common.ConfigLoader import ConfigLoader
from common.UserEntry import UserEntry
from discord import Member
from discord.ext.commands import Bot

class UserManager:
    """
    A class to manage user-related operations in the Discord bot.
    This class is responsible for handling things like if a user is even able to do something or if he is ignored by the bot.
    """
    accepted_users: set[Member] = set()
    bot_replies_users: set[Member] = set()

    @staticmethod
    def init(bot: Bot):
        """
        Initializes the UserManager by loading the accepted users from the configuration.
        if configuration None or empty, it will set accepted_users to an empty set.
        if configuration is "all", it will set accepted_users to all users in the bot's guilds.
        Will also update the user_database to contain all accepted users.
        :param bot: The bot instance to initialize the UserManager with, used to determine all users which the bot can see.
        """
        accepted_users_config = ConfigLoader.get_config().accepted_users
        UserManager.accepted_users = UserManager._get_users_from_config(accepted_users_config, bot)

        bot_replies_users_config = ConfigLoader.get_config().bot_replies_users
        UserManager.bot_replies_users = UserManager._get_users_from_config(bot_replies_users_config, bot)

        from database.DatabaseCollection import DatabaseCollection
        UserManager.user_database = DatabaseCollection.user_database
        for user in UserManager.accepted_users:
            DatabaseCollection.user_database.add_user(UserEntry(*(user.id,user.name,user.display_name)))

        print(f"UserManager initialized with accepted users: {UserManager.accepted_users}")
        print(f"UserManager initialized with bot replies users: {UserManager.bot_replies_users}\n")

    @staticmethod
    def _get_users_from_config(config_value: set[Member], bot: Bot):
        if config_value is None:
            return set()
        elif config_value == {"all"}:
            return {member for guild in bot.guilds for member in guild.members}
        else:
            return {member for guild in bot.guilds for member in guild.members if (
                    member.name in config_value or member.display_name in config_value)}

    @staticmethod
    def is_user_accepted(user_name: str) -> bool:
        """
        Checks if a user is accepted to use the bot.
        :param user_name: The name of the user to check.
        :return: True if user is accepted, False otherwise.
        """
        for member in UserManager.accepted_users:
            if member.name == user_name or member.display_name == user_name:
                return True

        print(f"User {user_name} is not accepted to use the bot.")
        return False

    @staticmethod
    def get_user_entry(user_id:int = None, user_name:str = None, display_name:str = None) -> UserEntry | None:
        """
        Gets a UserEntry object for a user based on their ID, username, or display name from the UserDatabase.
        :param user_id: The ID of the user to get the UserEntry for.
        :param user_name: The username of the user to get the UserEntry for.
        :param display_name: The display name of the user to get the UserEntry for.
        :return: A UserEntry object containing the user's information, or None if the user is not found.
        """
        if user_id:
            from database.DatabaseCollection import DatabaseCollection
            return DatabaseCollection.user_database.get_user_by_id(user_id)
        if user_name:
            ids = [member.id for member in UserManager.accepted_users if member.name == user_name]
            return UserManager.get_user_entry(user_id = ids[0]) if len(ids) > 0 else None
        if display_name:
            ids = [member.id for member in UserManager.accepted_users if member.display_name == display_name]
            return UserManager.get_user_entry(user_id = ids[0]) if len(ids) > 0 else None
        return None