"""Contains all new windows that may be created"""
from configparser import ConfigParser

import PySimpleGUI as sg

from src.modules import read_config
from src.modules.config_paths import CONFIG_PATH

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read(CONFIG_PATH)


def error_window(message: str):
    """Window made to tell the user what they're doing is wrong, and what to do instead
        :param message: Message to display to user
    """
    layout = [
        [sg.Text(message, text_color="red")],
    ]

    window = sg.Window("Error!", layout, finalize=True, keep_on_top=True)
    return window


def new_contact_window():
    layout = [
        # TODO: Make it so that all input boxes are even with each other.
        #  I've tried adding whitespace, and that has varying results so don't.
        #  Do for edit window as well.
        #  This isn't vital and I might not do it but we'll see
        [sg.Text("Name:"), sg.InputText(key="name")],
        [sg.Text("Email Address:"), sg.InputText(key="email")],
        [sg.Text("Phone Number:"), sg.InputText(key="phone")],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    window = sg.Window("Input Window", layout, finalize=True)
    return window


def row_selected_window(row_selected):
    """Window with options that appears when you select a row in the contacts table"""
    layout = [
        [sg.Text("What would you like to do with this contact?", justification="c")],
        [sg.Button("Edit", key="-EDIT-"), sg.Push(), sg.Button("Delete", key="-DELETE-")]
    ]

    window = sg.Window("Contact Settings", layout, finalize=True)
    return window


def edit_contact_window(json_dict):
    layout = [
        [sg.Text("Name:"), sg.InputText(json_dict["Name"], key="name")],
        [sg.Text("Email Address:"), sg.InputText(json_dict["Email Address"], key="email")],
        [sg.Text("Phone Number:"), sg.InputText(json_dict["Phone Number"], key="phone")],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    window = sg.Window("Edit Contact", layout, finalize=True)
    return window


def confirmation_window():
    layout = [
        [sg.Text("Are you sure you'd like to delete this contact? Press X to back out")],
        [sg.Button("Yes, banish them to the shadow realm", key="-ERADICATE-")]
    ]

    window = sg.Window("Delete Contact?", layout, element_justification="c", finalize=True)
    return window


def about_window():
    program_openings = read_config.return_stat("TimesProgramWasOpened")
    contacts_added = read_config.return_stat("AllTimeContactsAdded")
    empty_contact_attempts = read_config.return_stat("TimesYouTriedToAddAnEmptyContact")

    layout = [[sg.Image("./img/sg_logo.png")],
              [sg.Text("A PySimpleGui program \n       made by Banjo", font=("Arial", 20))],
              [sg.Text("Your Stats", font=("Arial", 15, "bold"))],
              [sg.Text(
                  f"Amount of times you opened this program: {program_openings}",
                  font=("Arial", 10))],
              [sg.Text(
                  f"Amount of times you've added a contact: {contacts_added}",
                  font=("Arial", 10))],
              [sg.Text(
                  f"Amount of times you tried to make an empty contact: {empty_contact_attempts}",
                  font=("Arial", 10))],
              [sg.Button("Take me to my configuration files", key="-CONFIG-TELEPORT-")],
              [sg.Button(
                  image_filename="./img/gh.png",
                  tooltip="This project's Github Repo!",
                  button_color=(sg.theme_background_color(), sg.theme_background_color()),
                  border_width=0,
                  image_subsample=10,  # Have to resort to using this because image_size was giving me problems
                  key="-GH-BUTTON-")],
              ]

    window = sg.Window("About", layout, finalize=True, element_justification="c", size=(400, 400))
    return window
