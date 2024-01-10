"""The default main window"""

import PySimpleGUI as sg
from src.modules import read_config
from configparser import ConfigParser

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read("./config.ini")

# if read_config.custom_window_size_bool():
#     window_size = (int(config.get("Config", "CustomWindowSizeX")), int(config.get("Config", "CustomWindowSizeY")))
# else:
#     window_size = (800, 600)

window_size = (800, 600)

sg.theme(read_config.get_usr_theme())

layout = [[sg.Text("Python Contact Book", size=400, font=("Arial", 25), justification="c")],
          # TODO: Make button that opens an add contact menu
          [sg.Submit("Add")]
          ]

window = sg.Window("Python Contact Book", layout, size=window_size, resizable=True, enable_close_attempted_event=True)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == "Cancel":

        # Writes updated config values to the file
        with open("config.ini", "w") as config_file:
            config.write(config_file)
        break

window.close()
