from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
import modules.login
from modules.confirmation_mail import Email
import re

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
        provided_password2 = self.password2_entry.get()


        def validate_input(self):
            

            if not re.match(r"[^@]+@[^@]+\.[^@]+", provided_email):
                messagebox.showerror("Invalid email", "Please enter a valid email address.")
                return False

            if len(provided_login) < 3 :
                messagebox.showerror("Invalid Login","Login should be at least 3 characters long")
                return False

            if len(provided_password) < 8 or not any(char.isupper() for char in provided_password) or not any(char.islower() for char in provided_password) or not any(char.isdigit() for char in provided_password):
                messagebox.showerror("Invalid password", "Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
                return False

            if provided_password != provided_password2:
                messagebox.showerror("Passwords don't match", "Please make sure the passwords match.")
                return False

            return True


        if validate_input(self):

            db = database_connect.DatabaseConnector()
            query = f"INSERT INTO users (username, password, email) VALUES ('{provided_login}', " \
                    f"crypt('{provided_password}', gen_salt('bf')), '{provided_email}');"
            db.make_query(query)

        
            email_sender = Email()
            email_sender.send_confirmation_mail_eng(provided_email, provided_login)

            self.get_me_to_login()



    def get_me_to_login(self):
        self.destroy()
        login_page = modules.login.Login()
        login_page.mainloop()
        
        