"""Edits values in the config"""
from src.modules import new_windows
from src.modules.config_paths import CONFIG_PATH, config


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
    try:
        if not config.has_section(section):
            config.add_section(section)
            print(f"{section} added")

        if not config.has_option(section, key):
            config.set(section, key, value)
            print(f"{key} added to {section} with value {value}")

        with open(CONFIG_PATH, "w") as f:
            config.write(f)

        # Reloads config file
        config.read(CONFIG_PATH)
    except FileNotFoundError:
        new_windows.error_window("There was an error finding your config file, please restart to generate a new one.")


def increment_key(section, key, increment_by):
    """Increments an INI value by a defined amount
        :param section: The section to find the value in
        :param key: The key to increment
        :param increment_by: the number to increment the value by
    """
    value_exists_safety(section, key, "0")

    try:
        current_value = config.getint(section, key)
        new_value = current_value + int(increment_by)

        config.set(section, key, str(new_value))

        with open(CONFIG_PATH, 'w') as config_file:
            config.write(config_file)

    except FileNotFoundError:
        new_windows.error_window("There was an error finding your config file, please restart to generate a new one.")
