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


class SpendLimit(customtkinter.CTk):
    def __init__(self, username):
        self.username = username
        super().__init__()
        self.geometry("600x400")
        self.title("Add monthly spend limit")
        self.resizable(True, True)
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=400)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.resizable(False, False)
        self.label = customtkinter.CTkLabel(master=self.frame, text="Change monthly spend limit", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="new")

        self.info_label = customtkinter.CTkLabel(master=self.frame, text="Enter value to set monthly spend limit:",
                                                     font=("arial", 25, "normal"))
        self.info_label.grid(column=0, row=1, columnspan=2, padx=20, pady=10)

        
        self.limit_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="", justify=CENTER)
        self.limit_entry.grid(column=0, row=2, padx=20, pady=10, sticky="ew")

        self.invite_button = customtkinter.CTkButton(master=self.frame, text="Set limit!",
                                                     command=lambda: self.set_limit(username))
        self.invite_button.grid(column=1, row=2, padx=20, pady=10)

        self.protocol('WM_DELETE_WINDOW', self.on_closing)


    def set_limit(self, username):
        try:
            limit = float(self.limit_entry.get())
            if limit > 0:
                db = database_connect.DatabaseConnector()
                query = f"UPDATE users SET spend_limit = {limit} WHERE username = '{self.username}';"
                db.make_query(query)
                messagebox.showinfo("Success", "Monthly spend limit has been set!")
                self.on_closing()
            else:
                messagebox.showerror("Error", "Value must be greater than 0!")
        except ValueError:
            messagebox.showerror("Error", "Value must be a number!")

    
    def on_closing(self):
        self.destroy()
        home = home_window.HomeWindow(self.username)
        home.mainloop()