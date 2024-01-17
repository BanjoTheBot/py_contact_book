"""The default main window"""

import json
import os
import platform
import shutil
import sys
import uuid
import webbrowser
from configparser import ConfigParser

import PySimpleGUI as sg

from src.modules import new_windows, read_config, write_config
from src.modules.config_paths import CONFIG_PATH, SAVED_CONTACTS, USR_CONFIG_DIR

# Since the file structure changes when the program is bundled in an exe, we have to check to see what state it's in,
# and then change the path the original config and json files are found in accordingly.
if getattr(sys, "freeze", False):
    # Running as a bundle in an exe (frozen)
    bundle_dir = sys.MEIPASS  # I don't know why it's whining, but it works, so I ain't touching it
else:
    # Running directly as a script
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Create configuration and json files in /(user home directory)/.config/banjo/py-contact-book
if not os.path.exists(USR_CONFIG_DIR):
    os.makedirs(USR_CONFIG_DIR)

if not os.path.exists(CONFIG_PATH):
    shutil.copy(os.path.join(bundle_dir, "config.ini"), CONFIG_PATH)

if not os.path.exists(SAVED_CONTACTS):
    shutil.copy(os.path.join(bundle_dir, "saved_contacts.json"), SAVED_CONTACTS)

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config keys to lowercase
config.read(CONFIG_PATH)

# This was originally going to be changeable,
# but they may end up being more difficult than I thought, due to icons and PySimpleGui's sheer amount of themes
window_theme = "DarkGray9"


def make_contacts_table():
    top_row = ["id", "Name", "Email", "Phone No."]
    rows = read_config.make_lists_from_contacts(SAVED_CONTACTS)

    contacts_table = sg.Table(values=rows, headings=top_row,
                              auto_size_columns=True,
                              display_row_numbers=False,
                              justification='center', key='-TABLE-',
                              enable_events=True,
                              expand_x=True,
                              expand_y=True,
                              enable_click_events=True)

    return contacts_table


def refresh_table(window):
    new_table = make_contacts_table()
    new_table = new_table.get()
    window['-TABLE-'].update(new_table)


def main():
    window_size = (800, 600)

    sg.theme(window_theme)

    contacts_table = make_contacts_table()

    layout = [[sg.Text("Python Contact Book", size=400, font=("Arial", 25), justification="c")],
              [sg.Button("Add"), sg.Push(), sg.Button("About")],
              [contacts_table]
              ]

    window = sg.Window("Python Contact Book", layout, size=window_size, resizable=True,
                       enable_close_attempted_event=True)

    write_config.increment_key("Stats", "TimesProgramWasOpened", "1")

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == "Cancel":
            break

        # Add new contact window
        if event == "Add":
            add_contact_window = new_windows.new_contact_window()

            while True:
                event, values_input = add_contact_window.read()

                if event == sg.WIN_CLOSED or event == "Cancel":
                    break

                if event == "Submit":
                    items_not_empty = 0

                    contact_to_add = {
                        "id": int(str(uuid.uuid1().int)[:5]),  # This shortens the uuid, while keeping it as an int.
                        "Name": values_input["name"],
                        "Email Address": values_input["email"],
                        "Phone Number": values_input["phone"]
                    }

                    # If only one item has been filled out (it will always be id), throw an error and stop
                    # the user from adding an empty contact
                    for entry_value in contact_to_add.values():
                        if entry_value != "":
                            items_not_empty += 1

                    if items_not_empty > 1:
                        with open(SAVED_CONTACTS, "r") as file:
                            data_list = json.load(file)
                            data_list.append(contact_to_add)

                        with open(SAVED_CONTACTS, "w") as file:
                            json.dump(data_list, file, indent=4)

                        refresh_table(window)

                        write_config.increment_key("Stats", "AllTimeContactsAdded", 1)
                    else:
                        new_windows.error_window("New contacts must have at least one entry with text in it")
                        write_config.increment_key("Stats", "TimesYouTriedToAddAnEmptyContact", 1)
                    break

            add_contact_window.close()

        if event == "-TABLE-":
            row_selected = [read_config.make_lists_from_contacts(SAVED_CONTACTS)[row] for row in values[event]]

            # For some reason when we refresh the table, the event is set to -TABLE- again,
            # but there is no row selected, so row_selected doesn't equal anything.
            # Since id_to_find is trying to assign itself to the first position of nothing, the program crashes
            # due to an out of range error.
            # Stopping anything from being assigned and making sure nothing happens after that fixes the crash,
            # but still refreshes the table, allowing everything to run as intended.
            if not row_selected:
                continue
            else:
                id_to_find = (row_selected[0])

            options_menu = new_windows.row_selected_window(row_selected)

            while True:
                event, values_input = options_menu.read()
                if event == sg.WIN_CLOSED or event == "Cancel":
                    break

                with open(SAVED_CONTACTS, 'r') as file:
                    data = json.load(file)

                if event == "-EDIT-":
                    for item in data:
                        if item["id"] == id_to_find[0]:
                            options_menu.close()
                            edit_window = new_windows.edit_contact_window(item)
                            while True:
                                event, values_input = edit_window.read()

                                if event == sg.WIN_CLOSED or event == "Cancel":
                                    break

                                if event == "Submit":
                                    items_not_empty = 0

                                    contact_to_add = {
                                        "Name": values_input["name"],
                                        "Email Address": values_input["email"],
                                        "Phone Number": values_input["phone"]
                                    }

                                    # If only one item has been filled out (it will always be id),
                                    # throw an error and stop the user from adding an empty contact
                                    for entry_value in contact_to_add.values():
                                        if entry_value != "":
                                            items_not_empty += 1

                                    if items_not_empty > 1:
                                        item["Name"] = values_input["name"]
                                        item["Email Address"] = values_input["email"]
                                        item["Phone Number"] = values_input["phone"]

                                    with open(SAVED_CONTACTS, "w") as file:
                                        json.dump(data, file, indent=4)

                                    refresh_table(window)
                                break
                            edit_window.close()

                if event == "-DELETE-":
                    confirmation = new_windows.confirmation_window()

                    options_menu.close()
                    while True:
                        event, values_input = confirmation.read()

                        if event == sg.WIN_CLOSED or event == "Cancel":
                            break

                        if event == "-ERADICATE-":
                            for item in data:
                                if list(item.values()) == row_selected[0]:
                                    data.remove(item)

                            with open(SAVED_CONTACTS, 'w') as file:
                                json.dump(data, file, indent=4)

                            refresh_table(window)
                            break
                    confirmation.close()

        if event == "About":
            about_window = new_windows.about_window()

            while True:
                event, values_input = about_window.read()
                if event == sg.WIN_CLOSED or event == "Cancel":
                    break

                if event == "-CONFIG-TELEPORT-":
                    match platform.system():
                        case "Windows":
                            os.system(f"explorer {USR_CONFIG_DIR}")
                        case "Linux":
                            os.system(f"xdg-open {USR_CONFIG_DIR}")
                        case "Darwin":  # macOS
                            os.system(f"open {USR_CONFIG_DIR}")
                        case _:
                            new_windows.error_window("Apparently, your OS is either not read correctly, "
                                                     "or you're not using Windows, Linux or macOS."
                                                     "\nPlease make an issue on the GitHub repo with information "
                                                     "regarding your OS.")
                if event == "-GH-BUTTON-":
                    webbrowser.open("https://github.com/BanjoTheBot/py_contact_book")
    window.close()


if __name__ == "__main__":
    main()
