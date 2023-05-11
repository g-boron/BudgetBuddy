from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class ApplicationSettings(customtkinter.CTk):
    def __init__(self, user_id):
        self.id = user_id
        super().__init__()
        self.geometry("600x800")
        self.title("Options")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.resizable(False, False)
        self.label = customtkinter.CTkLabel(master=self.frame, text="Settings", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="new")

        self.language_label = customtkinter.CTkLabel(master=self.frame, text="Choose a language from the following:",
                                                     font=("arial", 25, "normal"))
        self.language_label.grid(column=0, row=1, columnspan=2, padx=20, pady=10)

        self.language_button_pl = customtkinter.CTkButton(master=self.frame, text="polish",
                                                          font=("arial", 20, "normal"))
        self.language_button_pl.grid(column=0, row=2, padx=20, pady=10)

        self.language_button_en = customtkinter.CTkButton(master=self.frame, text="english",
                                                          font=("arial", 20, "normal"))
        self.language_button_en.grid(column=1, row=2, padx=20, pady=10)

        self.theme_label = customtkinter.CTkLabel(master=self.frame, text="Choose a theme from the following:",
                                                  font=("arial", 25, "normal"))
        self.theme_label.grid(column=0, row=3, columnspan=2, padx=20, pady=10)

        self.dark_button = customtkinter.CTkButton(master=self.frame, text="dark", font=("arial", 20, "normal"))
        self.dark_button.grid(column=0, row=4, padx=20, pady=10)

        self.light_button = customtkinter.CTkButton(master=self.frame, text="light", font=("arial", 20, "normal"))
        self.light_button.grid(column=1, row=4, padx=20, pady=10)

        self.invite_label = customtkinter.CTkLabel(master=self.frame, text="Invite someone to your budget:",
                                                   font=("arial", 25, "normal"))
        self.invite_label.grid(column=0, row=5, padx=20, pady=10, columnspan=2)

        self.email_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="email", justify=CENTER)
        self.email_entry.grid(column=0, row=6, padx=20, pady=10, sticky="ew")

        self.invite_button = customtkinter.CTkButton(master=self.frame, text="Invite to budget!")
        self.invite_button.grid(column=1, row=6, padx=20, pady=10)

