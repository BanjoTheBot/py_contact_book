"""The default main window"""

import PySimpleGUI as sg

from src.modules import read_config
from configparser import ConfigParser
import json

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read("./config.ini")

SAVED_CONTACTS = "saved_contacts.json"

window_theme = read_config.get_usr_theme()


def new_contact():
    # sg.theme(window_theme)
    layout = [
        # TODO: Make it so that all input boxes are even with each other.
        # I've tried adding whitespace, and that has varying results so don't.
        [sg.Text("Name:"), sg.InputText(key="name")],
        [sg.Text("Email Address:"), sg.InputText(key="email")],
        [sg.Text("Phone Number:"), sg.InputText(key="phone")],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    window = sg.Window("Input Window", layout, finalize=True)
    return window


def main():
    window_size = (800, 600)

    sg.theme(window_theme)

    layout = [[sg.Text("Python Contact Book", size=400, font=("Arial", 25), justification="c")],
              [sg.Button("Add")]
              ]

    window = sg.Window("Python Contact Book", layout, size=window_size, resizable=True,
                       enable_close_attempted_event=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == "Cancel":
            # Writes updated config values to the file
            with open("config.ini", "w") as config_file:
                config.write(config_file)
            break

        # Add new contact
        if event == "Add":
            add_contact_window = new_contact()

            while True:
                event, values_input = add_contact_window.read()

                if event == sg.WIN_CLOSED or event == "Cancel":
                    break

                if event == "Submit":
                    contact_to_add = {
                        "Name": values_input["name"],
                        "Email Address": values_input["email"],
                        "Phone Number": values_input["phone"]
                    }

                    with open(SAVED_CONTACTS, "r") as file:
                        data_list = json.load(file)
                        data_list.append(contact_to_add)

                    with open(SAVED_CONTACTS, "w") as file:
                        json.dump(data_list, file, indent=4)

                    break

            add_contact_window.close()
            # Keeps the whole application from closing when the add window is closed, as well as reloading everything
            main()

    window.close()


if __name__ == "__main__":
    main()
