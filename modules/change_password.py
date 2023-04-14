import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
import textwrap


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class ChangePassword(customtkinter.CTk):
    def __init__(self, user_login):
        self.username = user_login
        super().__init__()
        self.geometry("800x600")
        self.title("Change Password")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.window_flag = 1

        self.label = customtkinter.CTkLabel(master=self.frame, text="Change your password",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=18, padx=10, row=0, column=1)

        self.login_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="New password", justify=CENTER)
        self.login_entry.grid(pady=18, padx=10, row=1, column=1, sticky="ew")

        self.password_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Confirm new password", show="*",
                                                     justify=CENTER)
        self.password_entry.grid(pady=18, padx=10, row=2, column=1, sticky="ew")

        self.password_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Previous Password", show="*",
                                                     justify=CENTER)
        self.password_entry.grid(pady=18, padx=10, row=3, column=1, sticky="ew")

        self.button_login = customtkinter.CTkButton(master=self.frame, text="Save changes")
        self.button_login.grid(pady=18, padx=10, row=4, column=1, sticky="ew")

       

