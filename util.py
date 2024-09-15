import tkinter as tk
from tkinter import messagebox

def get_button(window, text, color, command, fg='white'):
    """
    Create and return a button widget.
    :param window: The parent window to place the button on.
    :param text: The text to display on the button.
    :param color: The background color of the button.
    :param command: The function to call when the button is clicked.
    :param fg: The text color of the button.
    :return: A button widget.
    """
    button = tk.Button(window, text=text, bg=color, command=command, fg=fg, font=("Arial", 14))
    return button

def get_image_label(window):
    """
    Create and return an image label widget.
    :param window: The parent window to place the label on.
    :return: A label widget for displaying images.
    """
    label = tk.Label(window)
    return label

def get_entry_text(window):
    """
    Create and return an entry widget.
    :param window: The parent window to place the entry on.
    :return: An entry widget for text input.
    """
    entry = tk.Entry(window, font=("Arial", 14))
    return entry

def get_text_label(window, text):
    """
    Create and return a text label widget.
    :param window: The parent window to place the label on.
    :param text: The text to display on the label.
    :return: A label widget for displaying text.
    """
    label = tk.Label(window, text=text, font=("Arial", 14), bg="#f0f0f0")
    return label

def msg_box(title, message):
    """
    Show a message box with the given title and message.
    :param title: The title of the message box.
    :param message: The message to display in the message box.
    """
    messagebox.showinfo(title, message)
