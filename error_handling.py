import sqlite3
from functools import wraps
import tkinter as tk
from tkinter import messagebox


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print(f"Calling function {func.__name__} with args: {args} kwargs: {kwargs}")
            return func(*args, **kwargs)
        except (sqlite3.Error, tk.TclError, AttributeError, ValueError, TypeError) as e:
            print(f"Exception in function {func.__name__}: {e}")
            messagebox.showerror(title="Error!", message=str(e))
    return wrapper



