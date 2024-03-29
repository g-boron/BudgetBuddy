from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.functions.notifications import *
from modules import home_window
from modules.functions.sharing_budgets import *

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

LIGHT_COLOR = "#fbfbfb"
DARK_COLOR = "#242424"
SYSTEM_BLUE = "#1f6aa5"
INVITATION_TEXT = "You have a invitation to budget sharing from "


class Notifications(customtkinter.CTk):
    def __init__(self, user_login):
        super().__init__()
        self.login = user_login
        self.geometry("900x600")
        self.title("Notifications")
        self.resizable(True, True)
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.resizable(False, False)
        self.show_all_notifications(user_login)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def accept_invitation(self, user_id, notification_num):
        """Inserts to database information about accepted budget sharing invitation"""
        notification_number = notification_num
        sharing_accounts_ids = []
        notifications_id = []
        all_notifications = get_all_user_notifications(user_id)
        my_id = get_user_id(self.login)
        for i in range(len(all_notifications)):
            sharing_accounts_ids.append(all_notifications[i][1])
            notifications_id.append(all_notifications[i][0])
        print(sharing_accounts_ids)
        msg_box = messagebox.askquestion('Accept invitation', 'Are you sure you want to accept the invitation?',
                                         icon='question')

        if msg_box == 'yes':
            validation = validate_sharing_budget(my_id, sharing_accounts_ids[notification_number])
            if validation is not None:
                msg_box = messagebox.showerror('Budget is already shared!', 'The user and you are already sharing a '
                                                                            'budget with each other!')
            else:
                insert_shared_budget_to_database(my_id, sharing_accounts_ids[notification_number])
                db = database_connect.DatabaseConnector()
                delete_query = f"DELETE FROM invites WHERE id = {notifications_id[notification_number]};"
                db.make_query(delete_query)
                self.destroy()
                home = home_window.HomeWindow(self.login)
                home.mainloop()

    def decline_invitation(self, user_id, notification_num):
        """Inserts to database information about declined budget sharing invitation"""
        notification_number = notification_num
        all_notifications = get_all_user_notifications(user_id)
        notifications_id = []
        number_of_notifications = len(all_notifications)
        for i in range(number_of_notifications):
            notifications_id.append(all_notifications[i][0])
        msg_box = messagebox.askquestion('Decline invitation', 'Are you sure you want to decline the invitation?',
                                         icon='question')

        if msg_box == 'yes':
            db = database_connect.DatabaseConnector()
            delete_query = f"DELETE FROM invites WHERE id = {notifications_id[notification_number]};"
            db.make_query(delete_query)
            self.destroy()
            home = home_window.HomeWindow(self.login)
            home.mainloop()

    def show_all_notifications(self, user_id):
        """Shows all user's notifications"""
        all_notifications = get_all_user_notifications(user_id)
        sender_id = []
        sender_name = []
        notification_id = []
        number_of_notifications = len(all_notifications)
        db = database_connect.DatabaseConnector()

        for i in range(number_of_notifications):
            sender_id.append(all_notifications[i][1])
            notification_id.append(all_notifications[i][0])
            name_query = f"SELECT name FROM users WHERE id = '{sender_id[i]}';"
            account_name = db.select_data(name_query, 'one')
            sender_name.append(account_name[0])

        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        for j in range(number_of_notifications):
            row_number = j + 1
            label = customtkinter.CTkLabel(master=self.frame, text="Notifications panel",
                                           font=("Arial", 30, "normal"))
            label.grid(row=0, column=0, padx=0, pady=10, columnspan=2, sticky="n")

            check_mark = customtkinter.CTkCheckBox(master=self.frame, text="",
                                                   command=lambda notification=int(notification_id[j]):
                                                   mark_notification_as_read(notification))
            check_mark.grid(pady=20, padx=10, row=row_number, column=0)

            invitation = customtkinter.CTkLabel(master=self.frame,
                                                text=(INVITATION_TEXT + f"{sender_name[j]}"),
                                                font=("Arial", 18, "normal"))
            invitation.grid(pady=20, padx=10, row=row_number, column=1)

            accept_button = customtkinter.CTkButton(master=self.frame, text="Accept", hover_color="green",
                                                    command=lambda notification_num=int(j):
                                                    self.accept_invitation(user_id, notification_num),
                                                    font=('Arial', 18, 'normal'))
            accept_button.grid(pady=20, padx=10, row=row_number, column=2)

            decline_button = customtkinter.CTkButton(master=self.frame, text="Decline", hover_color="red",
                                                     command=lambda notification_num=int(j):
                                                     self.decline_invitation(user_id, notification_num),
                                                     font=('Arial', 18, 'normal'))
            decline_button.grid(pady=20, padx=10, row=row_number, column=3)

# read notifications are greyed out
            if all_notifications[j][2]:
                invitation.configure(text_color="grey")
                check_mark.select()
        sender_name.clear()
        sender_id.clear()

    def on_closing(self):
        """Desecrates what will happen after closing the window"""
        self.destroy()
        home = home_window.HomeWindow(self.login)
        home.mainloop()
