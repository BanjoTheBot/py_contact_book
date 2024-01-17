"""Edits values in the config"""

from configparser import ConfigParser
from src.modules.config_paths import CONFIG_PATH

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read(CONFIG_PATH)


def increment_value(section, value, increment_by: int):
    """Increments an INI value by a defined amount
        :param section: The section to find the value in
        :param value: The value to increment
        :param increment_by: the number to increment the value by
    """
    current_value = config.getint(section, value)
    new_value = current_value + increment_by

    config.set(section, value, str(new_value))

    with open(CONFIG_PATH, 'w') as config_file:
        config.write(config_file)
