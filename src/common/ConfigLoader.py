import os
import yaml
import re

from common.Config import Config


class ConfigLoader:
    """
    A class to load configuration settings from a file.
    """
    config_path = "../resources/config.yaml"

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
                file.write("  accepted_users:\n")

    @staticmethod
    def load() -> Config:
        """
        Load the configuration from the specified file.
        """
        ConfigLoader.create_config_file_if_not_exists()

        with open(ConfigLoader.config_path, "r") as file:
            config_dict = yaml.safe_load(file)

            return Config(config_dict["bot"]["api_key"],config_dict["bot"]["command_prefix"],config_dict["bot"]["databases_folder_path"],config_dict["bot"]["accepted_users"])