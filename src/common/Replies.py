import discord
import os
import yaml
import random

class Replies:
    """
    A class to hold various replies used by the bot based on specific keywords in messages.
    Also handles if there should be a reply or not.
    """
    def __init__(self, replies_path: str):
        """
        Initializes the Replies class with a path for the file containing the replies
        :param replies_path: The path to the file containing the replies.
        """
        self.replies_file_path = replies_path

        self.create_replies_file_if_not_exists()

        with open(replies_path, 'r', encoding='utf-8') as file:
            self.replies = yaml.safe_load(file)

    def create_replies_file_if_not_exists(self):
        """
        Creates a replies file if it does not exist.
        """
        if not os.path.exists(self.replies_file_path):
            print(f"Creating replies file at: {self.replies_file_path}")
            with open(self.replies_file_path, "w") as file:
                file.write("# Replies for the Discord bot\n")
                file.write("\n# Basic replies (message contains 'bot')\n")
                file.write("bot:\n")
                file.write("  - 'Hi'\n")

    def get_random_reply(self, message:discord.Message, dictionary: dict) -> str:
        """
        Returns a random entry in the dictionary if the key is contained in the message.
        If the entry is a dictionary it will recursively call itself on this dictionary until it is a string.
        :param message: The Discord message to check for keywords.
        :param dictionary: The dictionary to get a random reply from.
        :return: The reply string.
        """
        for key in dictionary.keys():
            if isinstance(dictionary[key], list):
                return random.choice(dictionary[key])
            elif isinstance(dictionary[key], dict):
                return self.get_random_reply(dictionary[key])
        return None

    def handle_message(self,message: discord.Message) -> str:
        """
        Handles the message and decides if a reply should be sent based on the content of the message.
        :param message: The Discord message to handle.
        :return: The reply string if a reply is needed, otherwise None.
        """
        for key in self.replies.keys():
            if key in message.content.lower():
                if isinstance(self.replies[key], list):
                    return random.choice(self.replies[key])
                elif isinstance(self.replies[key], dict):
                    return self.get_random_reply(message,self.replies[key])
        return None