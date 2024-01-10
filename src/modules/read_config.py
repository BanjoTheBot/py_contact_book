"""Returns the values of settings defined in /config.ini/"""

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
