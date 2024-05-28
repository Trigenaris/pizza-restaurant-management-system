import tkinter as tk
from tkinter import ttk
import winsound


class CustomShowError(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.geometry("300x150")
        self.resizable(False, False)

        image = tk.PhotoImage(file="crazy_error_logo.png")
        error_label = ttk.Label(self, image=image)
        error_label.image = image
        error_label.grid(row=0, column=0, pady=15)

        message_label = ttk.Label(self, text=message)
        message_label.grid(row=0, column=1, padx=15, pady=15)

        ok_button = ttk.Button(self, text="Ok", command=self.destroy)
        ok_button.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

        self.transient(parent)
        self.grab_set()
        self.wait_window(self)


def custom_showerror(parent, title=None, message=None):
    CustomShowError(parent, title, message)
