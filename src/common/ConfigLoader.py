import os
from zoneinfo import available_timezones

import yaml
import re

from common.Config import Config

class ConfigLoader:
    """
    A class to load configuration settings from a file.
    """
    config_path = "../resources/config.yaml"
    config = None

    @staticmethod
    def get_config():
        if not ConfigLoader.config:
            ConfigLoader.config = ConfigLoader.load()
        return ConfigLoader.config

    def __init__(self, config_path: str = None):
        """
        Initializes the ConfigLoader with a specified configuration file path.
        If no path is provided, it defaults to "../resources/config.yaml".
        :param config_path: The path to the configuration file.
        """
        if config_path:
            self.set_config_path(config_path)

    @staticmethod
    def get_config_path() -> str:
        """
        Returns the path to the configuration file.
        """
        return ConfigLoader.config_path

    @staticmethod
    def set_config_path(config_path: str) -> None:
        """
        Sets the path to the configuration file.
        :param config_path: The new path to the configuration file.
        """
        correct_path_format_regex = r"([a-zA-Z\._]*[\/\\])*config.yaml"
        regex = re.compile(correct_path_format_regex)

        if regex.match(config_path):
            ConfigLoader.config_path = config_path
        else:
            raise ValueError(f"Invalid configuration path format: {config_path}. "
                             f"Expected format: {correct_path_format_regex}")

    @staticmethod
    def create_config_file_if_not_exists():
        """
        Create a configuration file if it does not exist.
        """
        if not os.path.exists(ConfigLoader.config_path):
            print(f"Creating configuration file at: {ConfigLoader.config_path}")
            with open(ConfigLoader.config_path, "w") as file:
                file.write("# Configuration file for the Discord bot\n")
                file.write("\n")
                file.write("# Discord bot configuration\n")
                file.write("bot:\n")
                file.write("  api_key:\n")
                file.write("  command_prefix: '%'\n")
                file.write("  databases_folder_path: '../resources/databases/'\n")
                file.write("  music_folder_path: '../resources/music/'\n")
                file.write("  create_emojis: True\n")
                file.write("  bot_replies: True\n")
                file.write("  bot_replies_to_links: False\n")
                file.write("  bot_replies_users:\n")
                file.write("     - all\n")
                file.write("  bot_replies_channels:\n")
                file.write("     - all\n")
                file.write("  accepted_users:\n")
                file.write("     - all\n")
                file.write("  consoles:\n")
                file.write("    test : test\n")
                file.write("IGDB:\n")
                file.write("  client_id:\n")
                file.write("  client_secret:\n")

    @staticmethod
    def load() -> Config:
        """
        Load the configuration from the specified file.
        """
        ConfigLoader.create_config_file_if_not_exists()

        with open(ConfigLoader.config_path, "r") as file:
            config_dict = yaml.safe_load(file)
            return Config(api_key=config_dict["bot"]["api_key"],
                          command_prefix=config_dict["bot"]["command_prefix"],
                          database_folder_path=config_dict["bot"]["databases_folder_path"],
                          music_folder_path=config_dict["bot"]["music_folder_path"],
                          create_emojis=config_dict["bot"]["create_emojis"],
                          bot_replies=config_dict["bot"]["bot_replies"],
                          bot_replies_to_links=config_dict["bot"]["bot_replies_to_links"],
                          bot_replies_users=set(config_dict["bot"]["bot_replies_users"]) if config_dict["bot"]["bot_replies_users"] else set(),
                          bot_replies_channels=set(config_dict["bot"]["bot_replies_channels"]) if config_dict["bot"]["bot_replies_channels"] else set(),
                          accepted_users=set(config_dict["bot"]["accepted_users"]) if config_dict["bot"]["accepted_users"] else set(),
                          consoles=config_dict["bot"]["consoles"],
                          igdb_client_id=config_dict["IGDB"]["client_id"],
                          igdb_client_secret=config_dict["IGDB"]["client_secret"])

    @staticmethod
    def update(variable: str, value):
        """
        Updates the variable in the configuration file with the given value.
        :param: variable: The variable to update.
        :param: value: The new value for the variable.
        """
        ConfigLoader.create_config_file_if_not_exists()

        config_dict = dict()

        with open(ConfigLoader.config_path, "r") as file:
            config_dict = yaml.safe_load(file)

        if variable not in config_dict["bot"].keys():
            raise KeyError(f"Variable '{variable}' not found in the configuration file.")
        config_dict["bot"][variable] = value

        with open(ConfigLoader.config_path, "w") as file:
            yaml.safe_dump(config_dict, file, default_flow_style=False, sort_keys=False)

        ConfigLoader.config = ConfigLoader.load()