from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import ImageTk
from modules.database import database_connect

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


class Register(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Register an account")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.wm_iconbitmap()
        self.icopath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.icopath)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)
        self.frame.grid_rowconfigure(6, weight=1)
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Enter your details", font=("Arial", 30, "normal"))
        self.label.grid(pady=18, padx=10, row=0, column=1)

        self.email_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="E-mail", justify=CENTER)
        self.email_entry.grid(pady=18, padx=10, row=1, column=1, sticky="ew")

        self.login_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Login", justify=CENTER)
        self.login_entry.grid(pady=18, padx=10, row=2, column=1, sticky="ew")

        self.password_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*",
                                                     justify=CENTER)
        self.password_entry.grid(pady=18, padx=10, row=3, column=1, sticky="ew")

        self.password2_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Repeat password", show="*",
                                                      justify=CENTER)
        self.password2_entry.grid(pady=18, padx=10, row=4, column=1, sticky="ew")

        self.button_register = customtkinter.CTkButton(master=self.frame, text="Register", command = self.register)
        self.button_register.grid(pady=18, padx=10, row=5, column=1, sticky="ew")

        self.button_login = customtkinter.CTkButton(master=self.frame, fg_color="transparent",
                                              text="Already have an account", font=("Arial", 12, "normal"),
                                              command=self.get_me_to_login)
        self.button_login.configure(width=50, height=20)
        self.button_login.grid(pady=10, padx=0, column=1, row=6)

    def register(self):
        provided_email = self.email_entry.get()
        provided_login = self.login_entry.get()
        provided_password = self.password_entry.get()
        db = database_connect.DatabaseConnector()
        query = f"INSERT INTO users (username, password, email) VALUES ('{provided_login}', " \
                f"crypt('{provided_password}', gen_salt('bf')), '{provided_email}');"
        db.make_query(query)

    def get_me_to_login(self):
        pass
        
        