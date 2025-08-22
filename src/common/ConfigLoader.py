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
    available_consoles =    {'PC':'<:PC:1218171109145575535>',
                            'NES':'<:NES:1218170822305382470>',
                            'SNES':'<:SNES:1218171067395211324>',
                            'GameBoy':'<:GameBoy:1218170693254905926>',
                            'GameBoy Advance':'<:GameBoyAdvance:1218170726582845591>',
                            'N64':'<:N64:1218170791120601159>',
                            'GameCube':'<:GameCube:1218170761861267537>',
                            'DS':'<:DS:1218170876860829707>',
                            '3DS':'<:3DS:1280970046272831549>',
                            'Wii':'<:Wii:1218171432756842587>',
                            'WiiU':'<:WiiU:1218171456639340614>',
                            'Switch':'<:Switch:1218171017512616016>',
                            'Switch 2':'<:Switch2:1369050664948203580>',
                            'Dreamcast':'<:Dreamcast:1218172336725823518>',
                            'Genesis':'<:Genesis:1218171327861489775>',
                            'MasterSystem':'<:MasterSystem:1218171369473183815>',
                            'Saturn':'<:Saturn:1218171402033827872>',
                            'XBOX':'<:XBOX:1218172368879358042>',
                            'XBOX 360':'<:XBOX360:1218171484951019622>',
                            'XBOX ONE':'<:XBOXONE:1218171506836639784>',
                            'PS1':'<:PS1:1218171162131959808>',
                            'PS2':'<:PS2:1218171210978820166>',
                            'PS3':'<:PS3:1218171132667232346>',
                            'PS4':'<:PS4:1218171295104110623>',
                            'PS5':'<:PS5:1227527850710536212>',
                            'PSP':'<:PSP:1286032971907993701>',
                            'PS Vita':'<:PSVita:1286032764201599077>'}

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
                file.write("  bot_replies: True\n")
                file.write("  bot_replies_to_links: False\n")
                file.write("  accepted_users:\n")
                file.write("  consoles:\n")
                for console in ConfigLoader.available_consoles.keys():
                    file.write(f"    {console}: '{ConfigLoader.available_consoles[console]}'\n")

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
                          bot_replies=config_dict["bot"]["bot_replies"],
                          bot_replies_to_links=config_dict["bot"]["bot_replies_to_links"],
                          accepted_users=set(config_dict["bot"]["accepted_users"]) if config_dict["bot"]["accepted_users"] else set(),
                          consoles=config_dict["bot"]["consoles"])