"""
This file is used for all files to get the correct config paths from.
It's being done here due to some issues with circular imports.
"""
import os

USR_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "banjo", "py-contact-book")
CONFIG_PATH = os.path.join(USR_CONFIG_DIR, "config.ini")
SAVED_CONTACTS = os.path.join(USR_CONFIG_DIR, "saved_contacts.json")
