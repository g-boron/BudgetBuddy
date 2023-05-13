from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.functions.notifications import *
from modules import home_window
from modules.functions.sharing_budgets import *

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

LIGHT_COLOR = "#fbfbfb"
DARK_COLOR = "#242424"
SYSTEM_BLUE = "#1f6aa5"
INVITATION_TEXT = "You have a invitation to budget sharing from "


class ChooseBudget(customtkinter.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.id = user_id #login
        self.geometry("400x600")
        self.title("Choose the budget you want to use.")
        self.resizable(True, True)
        self.frame = customtkinter.CTkFrame(master=self, width=400, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.label = customtkinter.CTkLabel(master=self.frame, text="Choose budget from the following",
                                            font=("Arial", 15, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10, columnspan=2, sticky="n")


