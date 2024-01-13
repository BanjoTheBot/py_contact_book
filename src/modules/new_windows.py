"""Contains all new windows that may be created"""
import PySimpleGUI as sg


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
