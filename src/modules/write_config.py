"""Edits values in the config"""

from configparser import ConfigParser

from src.modules.config_paths import CONFIG_PATH

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read(CONFIG_PATH)


def value_exists_safety(section: str, key: str, value: str):
    """
        Safety that checks to make sure an ini section or key exists before its written to.
        This is to ensure that in the event a new value has been added in an update or the user has gone and deleted it.
        If it is missing, we'll write the new value in. What this does mean though is that the ini file might be a bit
        unorganised compared to the official version.

        :param section: The section to check
        :param key: The key to check
        :param value: The default value to set the key to if the section and key don't exist
    """
    if not config.has_section(section):
        config.add_section(section)

    if not config.has_option(section, key):
        config.set(section, key, value)

    with open(CONFIG_PATH, "w") as f:
        config.write(f)


def increment_key(section, key, increment_by: str):
    """Increments an INI value by a defined amount
        :param section: The section to find the value in
        :param key: The key to increment
        :param increment_by: the number to increment the value by
    """
    value_exists_safety(section, key, "0")

    current_value = config.getint(section, key)
    new_value = current_value + int(increment_by)

    config.set(section, key, str(new_value))

    with open(CONFIG_PATH, 'w') as config_file:
        config.write(config_file)
