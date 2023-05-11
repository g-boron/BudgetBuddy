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
        self.geometry("900x900")
        self.title("Options")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.resizable(False, False)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Settings", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10, rowspan=5, sticky="n")

        self.language_label = customtkinter.CTkLabel(master=self.frame, text="Choose a language from the following:",
                                                     font=("arial", 25, "normal"))
        self.language_label.grid(column=0, row=1, rowspan=2, padx=20, pady=10)

        self.language_button_pl = customtkinter.CTkButton(master=self.frame, text="polish",
                                                          font=("arial", 20, "normal"))
        self.language_button_pl.grid(column=0, row=2, padx=20, pady=10)

        self.language_button_en = customtkinter.CTkButton(master=self.frame, text="english",
                                                          font=("arial", 20, "normal"))
        self.language_button_en.grid(column=1, row=2, padx=20, pady=10)
