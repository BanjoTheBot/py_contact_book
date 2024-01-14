"""Returns the values of settings defined in /config.ini/ and /saved_contacts.json/"""

import json
from configparser import ConfigParser

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read("./config.ini")


def get_usr_theme():
    """Returns the currently selected theme. Default is DarkGray9"""
    return config.get("Config", "UsrSelectedTheme")


def custom_window_size_bool():
    """Returns the value of RememberCustomWindowSize as a boolean"""
    return config.get("OptionSelect", "RememberCustomWindowSize") == "true"


def return_stat(stat):
    config.read("./config.ini")  # Reloads the ini so the stats window stays up to date
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
