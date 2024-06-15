import tkinter as tk
from tkinter import ttk
import winsound


class CustomMessageBoxes(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.message = message
        self.display_width = parent.winfo_screenwidth()
        self.display_height = parent.winfo_screenheight()
        self.left = int(self.display_width / 2 - (300 / 2))
        self.top = int(self.display_height / 2 - (150 / 2))
        self.geometry(f"300x150+{self.left}+{self.top}")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()


class CustomShowError(CustomMessageBoxes):
    def __init__(self, parent, title, message):
        super().__init__(parent, title, message)

        image = tk.PhotoImage(file="crazy_error_logo.png")
        error_label = ttk.Label(self, image=image)
        error_label.image = image
        error_label.grid(row=0, column=0, pady=15)

        message_label = ttk.Label(self, text=message)
        message_label.grid(row=0, column=1, padx=15, pady=15)

        ok_button = ttk.Button(self, text="Ok", command=self.destroy)
        ok_button.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

        self.wait_window(self)


class CustomShowInfo(CustomMessageBoxes):
    def __init__(self, parent, title, message):
        super().__init__(parent, title, message)

        image = tk.PhotoImage(file="crazy_showinfo_logo.png")
        error_label = ttk.Label(self, image=image)
        error_label.image = image
        error_label.grid(row=0, column=0, pady=15)

        message_label = ttk.Label(self, text=message)
        message_label.grid(row=0, column=1, padx=15, pady=15)

        ok_button = ttk.Button(self, text="Ok", command=self.destroy)
        ok_button.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

        self.wait_window(self)


def custom_showerror(parent, title=None, message=None):
    CustomShowError(parent, title, message)


def custom_showinfo(parent, title=None, message=None):
    CustomShowInfo(parent, title, message)
