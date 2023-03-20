import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class HomeWindow(customtkinter.CTk):
    def __init__(self, user_name):
        self.username = user_name
        print(self.username)
        super().__init__()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        '''self.login_instance = Login()
        self.user_name = self.login_instance.get_user_name()'''
        self.geometry("%dx%d" % (width, height))
        self.state('zoomed')
        self.title("Welcome to home window")
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_dark.png")
        self.iconphoto(False, self.iconpath)
        self.resizable(True, True)
        self.label = customtkinter.CTkLabel(master=self, text=f"Welcome, {self.get_user_name(self.username)}",
                                            font=("Arial", 30, "normal"))
        self.label.pack()

    def get_user_name(self, user_login):
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT name FROM users WHERE username='{user_login}';"
        user_name = db.select_data(name_query, 'one')
        return user_name[0]
