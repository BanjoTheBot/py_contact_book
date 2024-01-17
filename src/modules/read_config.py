"""Returns the values of settings defined in the config and json files"""

import json
from configparser import ConfigParser

from src.modules import write_config
from src.modules.config_paths import CONFIG_PATH

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read(CONFIG_PATH)


def get_usr_theme():
    """Returns the currently selected theme. Default is DarkGray9"""
    write_config.value_exists_safety("Config", "UsrSelectedTheme", "DarkGray9")
    return config.get("Config", "UsrSelectedTheme")


def return_stat(stat):
    write_config.value_exists_safety("Stats", stat, "0")
    config.read(CONFIG_PATH)  # Reloads the ini so the stats window stays up to date
    return config.get("Stats", stat)


def make_lists_from_contacts(json_file_path):
    """Makes a list of contact data in the json file
        :param json_file_path: The path for the JSON file.
    """
    with open(json_file_path, "r") as file:
        json_data = json.load(file)

    all_contacts_list = []

    for item in json_data:
        new_list = [item["id"], item["Name"], item["Email Address"], item["Phone Number"]]

        all_contacts_list.append(new_list)

    return all_contacts_list
