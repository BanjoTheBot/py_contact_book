"""Contains all new windows that may be created"""

import PySimpleGUI as sg

from src.modules import read_config
from src.modules.config_paths import IMG_CACHE


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


def edit_contact_window(contact_id):
    """Window that appears when you select a row in the contacts table.
        Contains more info about the contact, as well as options to edit them.
    """
    if read_config.return_pfp_exists_status(contact_id["id"]):
        pfp_path = f"{IMG_CACHE}/{contact_id["id"]}.png"
    else:
        pfp_path = f"{read_config.path_for_images()}/blank_pfp.png"

    layout = [
        [sg.Image(pfp_path)],
        [sg.InputText(key="-EDIT_PFP-",), sg.FileBrowse("Edit Picture",  file_types=(("Image Files", "*.png;*.jpg;*.jpeg"),))],
        [sg.Text("id:"), sg.Text(contact_id["id"])],
        [sg.Text("Name:"), sg.Push(), sg.InputText(contact_id["Name"], key="name")],
        [sg.Text("Email Address:"), sg.InputText(contact_id["Email Address"], key="email")],
        [sg.Text("Phone Number:"), sg.InputText(contact_id["Phone Number"], key="phone")],
        [sg.Button("Submit"), sg.Button("Cancel"),sg.Button("Delete", button_color="red", key="-DELETE-")]
    ]

    window = sg.Window(f"Edit {contact_id["Name"]}'s Contact", layout, finalize=True, element_justification="c")
    return window


def confirmation_window():
    layout = [
        [sg.Text("Are you sure you'd like to delete this contact? Press X to back out")],
        [sg.Button("Yes, banish them to the shadow realm", button_color="red", key="-ERADICATE-")]
    ]

    window = sg.Window("Delete Contact?", layout, element_justification="c", finalize=True)
    return window


def about_window():
    bundle_dir = read_config.path_for_images()

    program_openings = read_config.return_stat("TimesProgramWasOpened")
    contacts_added = read_config.return_stat("AllTimeContactsAdded")
    empty_contact_attempts = read_config.return_stat("TimesYouTriedToAddAnEmptyContact")

    layout = [[sg.Image(f"{bundle_dir}/sg_logo.png")],
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
                  image_filename=f"{bundle_dir}/gh.png",
                  tooltip="This project's Github Repo!",
                  button_color=(sg.theme_background_color(), sg.theme_background_color()),
                  border_width=0,
                  image_subsample=10,  # Have to resort to using this because image_size was giving me problems
                  key="-GH-BUTTON-")],
              ]

    window = sg.Window("About", layout, finalize=True, element_justification="c", size=(400, 400))
    return window
