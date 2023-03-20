from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import ImageTk
from modules.home_window import HomeWindow
from modules.database import database_connect

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class Login(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Login in to your account")
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
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.are_valid = False

        self.label = customtkinter.CTkLabel(master=self.frame, text="Enter your credentials",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=18, padx=10, row=0, column=1)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Login", justify=CENTER)
        self.entry1.grid(pady=18, padx=10, row=1, column=1, sticky="ew")

        self.entry2 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*", justify=CENTER)
        self.entry2.grid(pady=18, padx=10, row=2, column=1, sticky="ew")

        self.button_login = customtkinter.CTkButton(master=self.frame, text="Login", command=self.login)
        self.button_login.grid(pady=18, padx=10, row=3, column=1, sticky="ew")

        self.checkbox = customtkinter.CTkCheckBox(master=self.frame, text="Remember me")
        self.checkbox.grid(pady=18, padx=10, row=4, column=1)

        self.button = customtkinter.CTkButton(master=self.frame, fg_color="transparent",
                                              text="Forgot your password?", font=("Arial", 12, "normal"),
                                              command=self.forgot_password)
        self.button.configure(width=50, height=20)
        self.button.grid(pady=10, padx=0, column=0, row=5)

        self.button = customtkinter.CTkButton(master=self.frame, fg_color="transparent",
                                              text="Register an account!", font=("Arial", 12, "normal"),
                                              command=self.get_me_to_registration)
        self.button.configure(width=50, height=20)
        self.button.grid(pady=10, padx=0, column=2, row=5, rowspan=2, sticky="sw")

    def check_login_credentials(self):
        provided_username = self.entry1.get()
        provided_password = self.entry2.get()
        db = database_connect.DatabaseConnector()
        login_query = f"SELECT username, password FROM users WHERE username='{provided_username}';"
        user_pass = db.select_data(login_query, 'one')
        if user_pass is not None and provided_username == user_pass[0] and provided_password == user_pass[1]:
            return user_pass[0]
        else:
            return False

    def login(self):
        x = self.check_login_credentials()
        print(x)
        if x:
            self.destroy()
            home_window = HomeWindow(x)
            home_window.mainloop()
        else:
            messagebox.showerror(title="login or password not valid", message="Login or password do not match!")
        '''try:
            home_window = HomeWindow(x)
            home_window.mainloop()
            self.destroy()
        except:
            messagebox.showerror(title="login or password not valid", message="Login or password do not match!")'''

    def get_me_to_registration(self):
        pass

    def forgot_password(self):
        pass
