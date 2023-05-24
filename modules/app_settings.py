from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.functions.invite_to_budget import *
from modules import home_window


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

LIGHT_COLOR = "#fbfbfb"
DARK_COLOR = "#242424"
SYSTEM_BLUE = "#1f6aa5"


class ApplicationSettings(customtkinter.CTk):
    def __init__(self, user_id):
        self.id = user_id
        super().__init__()
        self.geometry("600x800")
        self.title("Options")
        self.resizable(True, True)
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.resizable(False, False)
        self.label = customtkinter.CTkLabel(master=self.frame, text="Settings", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="new")
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.language_label = customtkinter.CTkLabel(master=self.frame, text="Choose a language from the following:",
                                                     font=("arial", 25, "normal"))
        self.language_label.grid(column=0, row=1, columnspan=2, padx=20, pady=10)

        self.language_button_pl = customtkinter.CTkButton(master=self.frame, text="polish",
                                                          font=("arial", 20, "normal"),
                                                          command=self.change_ui_language_to_pl())
        self.language_button_pl.grid(column=0, row=2, padx=20, pady=10)

        self.language_button_en = customtkinter.CTkButton(master=self.frame, text="english",
                                                          font=("arial", 20, "normal"),
                                                          command=self.change_ui_language_to_eng())
        self.language_button_en.grid(column=1, row=2, padx=20, pady=10)

        self.theme_label = customtkinter.CTkLabel(master=self.frame, text="Choose a theme from the following:",
                                                  font=("arial", 25, "normal"))
        self.theme_label.grid(column=0, row=3, columnspan=2, padx=20, pady=10)

        self.dark_button = customtkinter.CTkButton(master=self.frame, text="dark", font=("arial", 20, "normal"),
                                                   fg_color=DARK_COLOR, hover_color=SYSTEM_BLUE,
                                                   command=lambda:self.change_ui_theme("dark"))
        self.dark_button.grid(column=0, row=4, padx=20, pady=10)

        self.light_button = customtkinter.CTkButton(master=self.frame, text="light", font=("arial", 20, "normal"),
                                                    fg_color=LIGHT_COLOR, hover_color=SYSTEM_BLUE,
                                                    command=lambda:self.change_ui_theme("light"))
        self.light_button.grid(column=1, row=4, padx=20, pady=10)

        self.invite_label = customtkinter.CTkLabel(master=self.frame, text="Invite someone to your budget:",
                                                   font=("arial", 25, "normal"))
        self.invite_label.grid(column=0, row=5, padx=20, pady=10, columnspan=2)

        self.login_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="login", justify=CENTER)
        self.login_entry.grid(column=0, row=6, padx=20, pady=10, sticky="ew")

        self.invite_button = customtkinter.CTkButton(master=self.frame, text="Invite to budget!",
                                                     command=lambda: self.invite_someone(user_id))
        self.invite_button.grid(column=1, row=6, padx=20, pady=10)

    def change_ui_theme(self, theme):
        db = database_connect.DatabaseConnector()

        if theme == "light":
            query = f"UPDATE users SET theme = 'light' WHERE username = '{self.id}'"
        elif theme == "dark":
            query = f"UPDATE users SET theme = 'dark' WHERE username = '{self.id}'"

        db.make_query(query)
            
    def on_closing(self):
        self.destroy()
        home = home_window.HomeWindow(self.id)
        home.mainloop()


    def change_ui_language_to_eng(self):
        pass

    def change_ui_language_to_pl(self):
        pass

    def invite_someone(self, user_id):
        inviting_person = user_id
        invited_person = self.login_entry.get()
        invited_login = str(invited_person)
        invite_a_friend(inviting_person, invited_login)
        self.destroy()

