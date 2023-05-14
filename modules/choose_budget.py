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

    def get_user_login(self, user_id):
        db = database_connect.DatabaseConnector()
        login_query = f"SELECT username FROM users WHERE id = {user_id};"
        result = db.select_data(login_query, 'one')
        return result

    def open_default_budget(self, user_id):
        self.destroy()
        home = home_window.HomeWindow(user_id)
        home.mainloop()

    '''def open_back_default_budget(self, user_id):
        id_user = user_id
        print(id_user)
        self.destroy()
        home = home_window.HomeWindow(id_user)
        home.mainloop()'''

    def get_to_budget(self, owner_id):
        account_id = owner_id
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT username FROM users WHERE id='{account_id}';"
        user_name = db.select_data(name_query, 'one')
        self.destroy()
        self.flag = True
        home = home_window.HomeWindow(user_name[0])
        home.mainloop()

    def get_to_dafault_budget(self, user_id, owner_id):
        user = int(get_user_id(user_id))
        owner = owner_id
        db = database_connect.DatabaseConnector()
        check_query = f"SELECT id, inheriting_id FROM shared_budgets WHERE owner_id = {owner} OR inheriting_id = {user};"
        check = db.select_data(check_query, 'one')
        if check is not None:
            return True, user
        else:
            return False

    def get_all_budgets(self, user_id):
        budget_id_list = []
        owner_id_list = []
        owner_name = []
        inheriting = get_user_id(user_id)
        db = database_connect.DatabaseConnector()
        query = f"SELECT id, owner_id FROM shared_budgets WHERE inheriting_id = {inheriting};"
        all_budgets = db.select_data(query)
        number_of_budgets = len(all_budgets)

        for i in range(number_of_budgets):
            budget_id_list.append((all_budgets[i][0]))
            owner_id_list.append(all_budgets[i][1])
            name_query = f"SELECT name FROM users WHERE id = '{owner_id_list[i]}';"
            account_name = db.select_data(name_query, 'one')
            owner_name.append(account_name[0])

        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        for j in range(number_of_budgets):
            check = self.get_to_dafault_budget(user_id, owner_id_list[j])
            row_number = j + 2
            self.label = customtkinter.CTkLabel(master=self.frame, text="Choose budget",
                                                font=("Arial", 30, "normal"))
            self.label.grid(row=0, column=0, padx=20, pady=10, columnspan=2, sticky="n")
            if check[0]:
                user_name = self.get_user_login(check[1])
                login = user_name[0]
                self.own_budget = customtkinter.CTkButton(master=self.frame, text="My budget",
                                                          font=("Arial", 18, "normal"),
                                                          command=lambda: self.open_default_budget(user_id=login))
                self.own_budget.grid(pady=20, padx=10, row=1, column=0, sticky="ew")

            else:
                self.own_budget = customtkinter.CTkButton(master=self.frame, text="Get back to my budget",
                                                          font=("Arial", 18, "normal"),
                                                          command=self.open_default_budget(user_id=self.id))
                self.own_budget.grid(pady=20, padx=10, row=1, column=0, sticky="ew")

            self.budget = customtkinter.CTkButton(master=self.frame, text=(TEXT + f"{owner_name[j]}"),
                                                  font=("Arial", 18, "normal"),
                                                  command=lambda owner_id=owner_id_list[j]:
                                                  self.get_to_budget(owner_id))
            self.budget.grid(pady=20, padx=10, row=row_number, column=0, sticky="ew")

        budget_id_list.clear()
        owner_id_list.clear()
        owner_name.clear()

    def on_closing(self):
        self.destroy()
        home = home_window.HomeWindow(self.id)
        home.mainloop()


