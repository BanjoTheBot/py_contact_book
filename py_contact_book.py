"""The default main window"""

import json
import uuid
import webbrowser
from configparser import ConfigParser

import PySimpleGUI as sg

from src.modules import new_windows, read_config, write_config

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read("./config.ini")

SAVED_CONTACTS = "saved_contacts.json"

# This was originally going to be changeable,
# but they may end up being more difficult than I thought, due to icons and PySimpleGui's sheer amount of themes
window_theme = read_config.get_usr_theme()


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

    write_config.increment_value("Stats", "TimesProgramWasOpened", 1)

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
                        # TODO: The id is at the top for readability,
                        #  but find a way so that it's displayed last (or not at all) on the table.
                        #  Shouldn't be too hard.
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

                        # Automatically refreshes table with new contact
                        new_table = make_contacts_table()
                        new_table = new_table.get()
                        window['-TABLE-'].update(new_table)

                        write_config.increment_value("Stats", "AllTimeContactsAdded", 1)
                    else:
                        new_windows.error_window("New contacts must have at least one entry with text in it")
                        write_config.increment_value("Stats", "TimesYouTriedToAddAnEmptyContact", 1)
                    break

            add_contact_window.close()

        if event == "About":
            about_window = new_windows.about_window()

            while True:
                event, values_input = about_window.read()
                if event == sg.WIN_CLOSED or event == "Cancel":
                    break

                if event == "-GH-BUTTON-":
                    webbrowser.open("https://github.com/BanjoTheBot/py_contact_book")
    window.close()


if __name__ == "__main__":
    main()
