import modules.expense_edit
import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from modules.expense_edit import EditExpense
from modules import all_expenses


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class ExpenseDetail(customtkinter.CTk):
    def __init__(self, expense_id, username):
        self.id = expense_id
        self.username = username
        super().__init__()
        self.geometry("800x600")
        self.title("Expense detail")
        self.frame = customtkinter.CTkScrollableFrame(master=self, width=700, height=500)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.window_flag = 1

        db = database_connect.DatabaseConnector()
        query = f"SELECT expenses.name, expenses.description, expenses.add_date, expenses.amount, categories.name, " \
                f"expenses.id, users.currency FROM expenses JOIN categories ON expenses.category_id=categories.id " \
                f"JOIN users ON expenses.user_id=users.id WHERE expenses.id={self.id}"
        expense = db.select_data(query, 'one')

        self.name = customtkinter.CTkLabel(master=self.frame, text=expense[0], font=("Arial", 30, "normal"),
                                           wraplength=200)
        self.name.grid(pady=18, padx=10, row=0, column=0, sticky='nw')

        self.category = customtkinter.CTkLabel(master=self.frame, text=expense[4], font=("Arial", 30, "normal"))
        self.category.grid(pady=18, padx=10, row=0, column=1, sticky='n')

        self.date = customtkinter.CTkLabel(master=self.frame, text=str(expense[2]).split(' ')[0],
                                           font=("Arial", 30, "normal"))
        self.date.grid(pady=18, padx=10, row=0, column=2, sticky='ne')

        self.desc = customtkinter.CTkLabel(master=self.frame, text=expense[1], font=("Arial", 30, "normal"),
                                           wraplength=700)
        self.desc.grid(pady=18, padx=10, row=1, column=0, columnspan=3)

        self.amount = customtkinter.CTkLabel(master=self.frame, text=str(expense[3]) + ' ' + expense[6],
                                             font=("Arial", 30, "normal"), bg_color='#424543')
        self.amount.grid(pady=18, padx=10, row=2, column=0, sticky='sw')
        id_expense = expense[5]
        self.edit = customtkinter.CTkButton(master=self.frame, text="Edit expense", font=("Arial", 25, "normal"),
                                            command=lambda id_expense=id_expense: self.edit_expense(id_expense, username))
        self.edit.grid(row=3, column=0, padx=10, pady=20, sticky='sw')

        self.delete = customtkinter.CTkButton(master=self.frame, text="Delete expense",
                                              font=("Arial", 25, "normal"))
        self.delete.grid(row=3, column=2, padx=10, pady=20, sticky='sw')

        self.protocol('WM_DELETE_WINDOW', self.on_closing)


    def on_closing(self):
        self.destroy()
        expenses = all_expenses.AllExpenses(self.username)
        expenses.mainloop()

    def edit_expense(self, id_expense, username):
        db = database_connect.DatabaseConnector()
        query = f"SELECT id FROM users WHERE username='{username}'"
        user_id = db.select_data(query, 'one')[0]
        edit_window = modules.expense_edit.EditExpense(id_expense, user_id)
        self.destroy()
        edit_window.mainloop()
