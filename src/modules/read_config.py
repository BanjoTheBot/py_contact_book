"""Returns the values of settings defined in the config and json files, as well as various system values and states."""

import json
import os
import sys
from configparser import ConfigParser
from PIL import Image

from src.modules import write_config
from src.modules.config_paths import CONFIG_PATH, IMG_CACHE

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


def return_pfp_exists_status(contact_id):
    """Checks the cached images folder to see if the contact has a profile picture,
        If it does, it must also check to see it has the correct properties (file type, size)
    """

    for file in os.listdir(IMG_CACHE):
        file_path = os.path.join(IMG_CACHE, file)

        # Check if it's a regular file
        if os.path.isfile(file_path):
            file_name, file_extension = os.path.splitext(file)
            if file_name == str(contact_id):
                if file_extension == ".png":
                    image = Image.open(file_path)  # Opens the image with Pillow, allowing us to check it's size properties
                    if image.height == 300 and image.width == 300:
                        return True
    return False


def path_for_images():
    """Returns the correct path based on if the program is bundled or running as a script"""
    if hasattr(sys, '_MEIPASS'):
        # Running as a bundle in an exe (frozen)
        bundle_dir = f"{sys._MEIPASS}/img"
    else:
        # Running directly as a script
        bundle_dir = "./img"  # I don't know why it's whining, but it works, so I ain't touching it

    return bundle_dir


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
