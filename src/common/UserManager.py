from discord import Member
from common.ConfigLoader import ConfigLoader
from discord.ext.commands import Bot

class UserManager:
    """
    A class to manage user-related operations in the Discord bot.
    This class is responsible for handling things like if a user is even able to do something or if he is ignored by the bot.
    """
    accepted_users: set[Member] = set()

    @staticmethod
    def init(bot: Bot):
        """
        Initializes the UserManager by loading the accepted users from the configuration.
        if configuration None or empty, it will set accepted_users to an empty set.
        if configuration is "all", it will set accepted_users to all users in the bot's guilds.
        :param bot: The bot instance to initialize the UserManager with, used to determine all users which the bot can see.
        """
        accepted_users_config = ConfigLoader.get_config().accepted_users

        if accepted_users_config is None:
            UserManager.accepted_users = set()
        elif accepted_users_config == {"all"}:
            UserManager.accepted_users = {member for guild in bot.guilds for member in guild.members}
        else:
            UserManager.accepted_users = {member for guild in bot.guilds for member in guild.members if (
                        member.name in accepted_users_config or member.display_name in accepted_users_config)}

        print(f"UserManager initialized with accepted users: {UserManager.accepted_users}")

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
    def get_display_name(user_name: str) -> str | None:
        """
        Gets the display name of a user by their username.
        :param user_name: The name of the user to get the display name for.
        :return: The display name of the user, or None if the user is not found.
        """
        for member in UserManager.accepted_users:
            if member.name == user_name or member.display_name == user_name:
                return member.display_name
        return None

    @staticmethod
    def get_user_name(display_name: str) -> str | None:
        """
        Gets the username of a user by their display name.
        :param display_name: The display name of the user to get the username for.
        :return: The username of the user, or None if the user is not found.
        """
        for member in UserManager.accepted_users:
            if member.name == display_name or member.display_name == display_name:
                return member.name
        return None