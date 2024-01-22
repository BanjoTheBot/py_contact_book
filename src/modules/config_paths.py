"""
This file is used for all files to get the correct config paths from.
It's being done here due to some issues with circular imports.
"""
import os
from configparser import ConfigParser

USR_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "banjo", "py-contact-book")
CONFIG_PATH = os.path.join(USR_CONFIG_DIR, "config.ini")
SAVED_CONTACTS = os.path.join(USR_CONFIG_DIR, "saved_contacts.json")
IMG_CACHE = os.path.join(USR_CONFIG_DIR, "img_cache")

# Initialise config parser and show it where the config file is
# This is used by all files accessing the config file
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read(CONFIG_PATH)
