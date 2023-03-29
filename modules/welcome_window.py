import customtkinter
from tkinter import messagebox
from PIL import ImageTk
from modules.home_window import HomeWindow
from modules.database import database_connect

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class WelcomeWindow(customtkinter.CTk):
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
        self.label.grid(pady=18, padx=10, row=1, column=1)

        self.name_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="name",
                                                 justify=customtkinter.CENTER)
        self.name_entry.grid(pady=18, padx=10, row=3, column=1, sticky="ew")

        self.balance_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="bank balance",
                                                    justify=customtkinter.CENTER)
        self.balance_entry.grid(pady=18, padx=10, row=4, column=1, sticky="ew")

        self.button = customtkinter.CTkButton(master=self.frame, text="Confirm!",
                                              command=self.get_me_to_home_window)
        self.button.grid(pady=18, padx=10, row=5, column=1, sticky="ew")

    def validate(self):
        name = int(self.name_entry.get())
        balance = float(self.balance_entry.get())
        if name is not None and balance is not None:
            self.get_me_to_home_window()
        else:
            messagebox.showerror(title="Please fill both information!",
                                 message="One of the boxes is empty or has a bad value.")

    def get_me_to_home_window(self):
        name = self.name_entry.get()
        balance = self.balance_entry.get()
        x = self.userlogin
        print(x)
        if x:
            db = database_connect.DatabaseConnector()
            set_name_query = f" UPDATE users SET name = '{name}', balance = '{balance}' WHERE username = '{x}';"
            db.make_query(set_name_query)
            self.destroy()
            home_window = HomeWindow(x)
            home_window.mainloop()
        else:
            messagebox.showerror(title="error2", message="Something went wrong")

