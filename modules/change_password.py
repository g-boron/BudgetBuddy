import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
import textwrap
from tkinter import messagebox
import psycopg2


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

        self.password = customtkinter.CTkEntry(master=self.frame, placeholder_text="New password", show="*",
                                               justify=CENTER)
        self.password.grid(pady=18, padx=10, row=1, column=1, sticky="ew")

        self.password2 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Confirm new password", show="*",
                                                justify=CENTER)
        self.password2.grid(pady=18, padx=10, row=2, column=1, sticky="ew")

        self.password_old = customtkinter.CTkEntry(master=self.frame, placeholder_text="Previous Password", show="*",
                                                   justify=CENTER)
        self.password_old.grid(pady=18, padx=10, row=3, column=1, sticky="ew")

        self.button_save = customtkinter.CTkButton(master=self.frame, text="Save changes", command=self.save_changes)
        self.button_save.grid(pady=18, padx=10, row=4, column=1, sticky="ew")

    def save_changes(self):
        """Saves the changes to database"""
        password_old = self.password_old.get()
        password = self.password.get()
        password2 = self.password2.get()

        if password != password2:
                messagebox.showerror("New passwords don't match", "Please make sure the passwords match.")
                return False
        
        if len(password) < 8 or not any(char.isupper() for char in password) or \
                not any(char.islower() for char in password) or not any(char.isdigit() for char in password):
                messagebox.showerror("Invalid password", "Password should be at least 8 characters long and "
                                                         "contain at least one uppercase letter, one lowercase "
                                                         "letter, and one digit.")
                return False

        db = database_connect.DatabaseConnector()

        query = f"SELECT password FROM users WHERE username = '{self.username}' " \
                f"AND password = crypt('{password_old}', password);"
        user_pass = db.select_data(query, 'one')

        if user_pass is None:
            messagebox.showerror("Invalid password", "Old password incorrect")
            return False 

        if user_pass is not None:
            messagebox.showinfo("Success", "Password has been changed.")

            query_update = f"UPDATE users SET password = crypt('{password}', gen_salt('bf')) WHERE username = " \
                           f"'{self.username}';"
            result = db.make_query(query_update)
            self.destroy()
            return False
