from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.functions.notifications import *
import textwrap

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

LIGHT_COLOR = "#fbfbfb"
DARK_COLOR = "#242424"
SYSTEM_BLUE = "#1f6aa5"
INVITATION_TEXT = "You have a invitation to budget sharing from "

class Notifications(customtkinter.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.id = user_id
        self.geometry("800x600")
        self.title("Notifications")
        self.resizable(True, True)
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.resizable(False, False)
        self.label = customtkinter.CTkLabel(master=self.frame, text="Notifications panel", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10, columnspan=3, sticky="new")
        self.show_all_notifications(user_id)

    def accept_invitation(self):
        pass

    def declince_invitation(self):
        pass

    def show_all_notifications(self, user_id):
        all_notifications = get_all_user_notifications(user_id)
        sender_id = []
        sender_name = []
        number_of_notifications = len(all_notifications)
        db = database_connect.DatabaseConnector()

        for i in range(number_of_notifications):
            sender_id.append(all_notifications[i][1])
            name_query = f"SELECT name FROM users WHERE id = '{sender_id[i]}';"
            account_name = db.select_data(name_query, 'one')
            sender_name.append(account_name[0])

        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        for j in range(number_of_notifications):
            row_number = j + 1
            self.invitation = customtkinter.CTkLabel(master=self.frame,
                                                     text=(INVITATION_TEXT + f"{sender_name[j]}"),
                                                     font=("Arial", 18, "normal"))
            self.invitation.grid(pady=20, padx=10, row=row_number, column=0)

            self.accept_button = customtkinter.CTkButton(master=self.frame, text="Accept", hover_color="green",
                                                         command=lambda: self.accept_invitation(),
                                                         font=('Arial', 18, 'normal'),)
            self.accept_button.grid(pady=20, padx=10, row=row_number, column=1)

            self.declince_button = customtkinter.CTkButton(master=self.frame, text="Decline", hover_color="red",
                                                           command=lambda: self.declince_invitation(),
                                                           font=('Arial', 18, 'normal'),)
            self.declince_button.grid(pady=20, padx=10, row=row_number, column=2)
        sender_name.clear()
        sender_id.clear()




