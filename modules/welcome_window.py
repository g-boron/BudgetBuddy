import customtkinter
from PIL import ImageTk
import modules.register
from modules.database import database_connect

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class WelcomeWindow(customtkinter):
    def __init__(self, user_login):
        super().__init__()
        self.userlogin = user_login
        print(self.userlogin)
        self.geometry("800x600")
        self.title("Let us know something more about yourself")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.wm_iconbitmap()
        self.icopath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.icopath)
        self.frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.window_flag = 1

        self.label = customtkinter.CTkLabel(master=self.frame, text="Please fill the boxes",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=18, padx=10, row=0, column=1)

        self.name_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="name",
                                                  justify=customtkinter.CENTER)
        self.name_entry.grid(pady=18, padx=10, row=1, column=1, sticky="ew")

        self.login_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="bank balance",
                                                  justify=customtkinter.CENTER)
        self.login_entry.grid(pady=18, padx=10, row=2, column=1, sticky="ew")

