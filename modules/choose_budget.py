from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.functions.notifications import *
from modules import home_window
from modules.functions.sharing_budgets import *
from modules.functions.get_user_login import *
from modules.functions.get_user_id import *
from modules.functions.get_user_name import *


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

LIGHT_COLOR = "#fbfbfb"
DARK_COLOR = "#242424"
SYSTEM_BLUE = "#1f6aa5"
TEXT = "Shared budget with "


class ChooseBudget(customtkinter.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.id = user_id #login
        self.geometry("400x600")
        self.title("Choose the budget you want to use.")
        self.resizable(True, True)
        self.frame = customtkinter.CTkFrame(master=self, width=400, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.get_all_budgets(self.id)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def open_default_budget(self, user_id):
        self.destroy()
        home = home_window.HomeWindow(user_id)
        home.mainloop()

    def get_to_budget(self, owner_id):
        account_id = owner_id
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT username FROM users WHERE id='{account_id}';"
        user_name = db.select_data(name_query, 'one')
        self.destroy()
        home = home_window.HomeWindow(user_name[0])
        home.mainloop()

    def get_all_budgets(self, user_id):
        budget_id_list = []
        owner_id_list = []
        owner_name = []
        inheriting = get_user_id(user_id)
        db = database_connect.DatabaseConnector()
        query = f"SELECT id, owner_id FROM shared_budgets WHERE inheriting_id = {inheriting} OR owner_id = {inheriting};"
        all_budgets = db.select_data(query)
        number_of_budgets = len(all_budgets)
        home_window.is_not_default_budget = 1
        for i in range(number_of_budgets):
            budget_id_list.append((all_budgets[i][0]))
            owner_id_list.append(all_budgets[i][1])
            name_query = f"SELECT name FROM users WHERE id = '{owner_id_list[i]}';"
            account_name = db.select_data(name_query, 'one')
            owner_name.append(account_name[0])

        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        for j in range(number_of_budgets):
            check = check_if_user_is_an_owner(user_id)
            print("check: ", check)
            row_number = j + 2
            label = customtkinter.CTkLabel(master=self.frame, text="Choose budget", font=("Arial", 30, "normal"))
            label.grid(row=0, column=0, padx=20, pady=10, columnspan=2, sticky="n")
            if not check:
                login = self.id
                home_window.is_not_default_budget = 1
                own_budget = customtkinter.CTkButton(master=self.frame, text="My budget", font=("Arial", 18, "normal"),
                                                     command=lambda: self.open_default_budget(user_id=login))
                own_budget.grid(pady=20, padx=10, row=1, column=0, sticky="ew")

                budget = customtkinter.CTkButton(master=self.frame, text=(TEXT + f"{owner_name[j]}"),
                                                 font=("Arial", 18, "normal"),
                                                 command=lambda owner_id=owner_id_list[j]: self.get_to_budget(owner_id))
                budget.grid(pady=20, padx=10, row=row_number, column=0, sticky="ew")
            elif check:
                home_window.is_not_default_budget = 0
                check_def_budget = check_default_budget(user_id)
                if check_def_budget:
                    users_default_budget = get_default_budget(self.id)
                    own_budget = customtkinter.CTkButton(master=self.frame, text="My budget",
                                                         font=("Arial", 18, "normal"),
                                                         command=lambda: self.open_default_budget(user_id=login))
                    own_budget.grid(pady=20, padx=10, row=1, column=0, sticky="ew")
                    inherit_budget = customtkinter.CTkButton(master=self.frame, text="Get back to my budget",
                                                             font=("Arial", 18, "normal"),
                                                             command=self.get_to_budget(users_default_budget))
                    inherit_budget.grid(pady=20, padx=10, row=1, column=0, sticky="ew")
                else:
                    own_budget = customtkinter.CTkButton(master=self.frame, text="My budget",
                                                         font=("Arial", 18, "normal"),
                                                         command=lambda: self.open_default_budget(user_id=login))
                    own_budget.grid(pady=20, padx=10, row=1, column=0, sticky="ew")

        budget_id_list.clear()
        owner_id_list.clear()
        owner_name.clear()

    def on_closing(self):
        self.destroy()
        home = home_window.HomeWindow(self.id)
        home.mainloop()


