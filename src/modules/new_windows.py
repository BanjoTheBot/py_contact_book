"""Contains all new windows that may be created"""
from configparser import ConfigParser

import PySimpleGUI as sg

from src.modules import read_config

# Initialise config parser and show it where the config file is
config = ConfigParser()
config.optionxform = str  # This should (hopefully) stop ConfigParser changing config values to lowercase
config.read("./config.ini")


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
        [sg.Text("Name:"), sg.InputText(key="name")],
        [sg.Text("Email Address:"), sg.InputText(key="email")],
        [sg.Text("Phone Number:"), sg.InputText(key="phone")],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    window = sg.Window("Input Window", layout, finalize=True)
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
              [sg.Button(
                  image_filename="./img/gh.png",
                  button_color=(sg.theme_background_color(), sg.theme_background_color()),
                  border_width=0,
                  image_subsample=10,  # Have to resort to using this because image_size was giving me problems
                  key="-GH-BUTTON-")],
              ]

    window = sg.Window("About", layout, finalize=True, element_justification="c", size=(400, 360))
    return window
