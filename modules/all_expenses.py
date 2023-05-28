import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from modules.expense_detail import ExpenseDetail
from modules.add_expense import AddExpense
from modules import home_window
import textwrap
import csv
import json
from modules.functions.get_users_info import get_user_name

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class AllExpenses(customtkinter.CTk):
    def __init__(self, user_login):
        self.username = user_login
        super().__init__()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.state('zoomed')
        self.title("See all your expenses")
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.resizable(True, True)
        self.label = customtkinter.CTkLabel(master=self, text=f"{self.get_user_name(self.username)[1]}'s expenses",
                                            font=("Arial", 50, "normal"))
        self.label.pack(pady=50)

        self.label_cat = customtkinter.CTkLabel(master=self, text='Select category', font=('Arial', 35, 'normal'))
        self.label_cat.place(x=550, y=150)

        db = database_connect.DatabaseConnector()
        query = 'SELECT name FROM categories'
        results = db.select_data(query)
        categories = [r[0] for r in results]
        categories.insert(0, 'All')

        self.category_opt = customtkinter.CTkOptionMenu(self, values=categories, font=('Arial', 30, 'normal'))
        self.category_opt.place(x=800, y=155)

        self.expense_name_entry = customtkinter.CTkEntry(master=self, placeholder_text="name", justify=CENTER,
                                                         font=('Arial', 30, 'normal'))
        self.expense_name_entry.place(x=1000, y=150)

        self.filter_opt = customtkinter.CTkOptionMenu(self, values=['Date descending', 'Date ascending',
                                                                    'Amount descending', 'Amount ascending'],
                                                      font=('Arial', 30, 'normal'))
        self.filter_opt.place(x=1150, y=150)

        self.frame = customtkinter.CTkScrollableFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.refresh('All')

        self.add_button = customtkinter.CTkButton(master=self, text='Add new expense', command=self.add_new_expense,
                                                  font=('Arial', 30, 'normal'))
        self.add_button.place(relx=0.1, rely=0.9, anchor='center')

        self.refresh_button = customtkinter.CTkButton(master=self, text='Refresh',
                                                      command=lambda: self.refresh(str(self.category_opt.get())),
                                                      font=('Arial', 30, 'normal'))
        self.refresh_button.place(relx=0.375, rely=0.9, anchor='center')

        self.format_type = customtkinter.CTkOptionMenu(master=self, values=['csv', 'json'], font=('Arial', 30, 'normal'))
        self.format_type.place(relx=0.675, rely=0.9, anchor='center')

        self.download_button = customtkinter.CTkButton(master=self, text='Download',
                                                       command=lambda: self.download_data(str(self.category_opt.get())),
                                                       font=('Arial', 30, 'normal'))
        self.download_button.place(relx=0.59, rely=0.9, anchor='center')

        self.exit_button = customtkinter.CTkButton(master=self, text='Exit', command=lambda: self.on_closing(),
                                                   font=('Arial', 30, 'normal'))
        self.exit_button.place(relx=0.9, rely=0.9, anchor='center')

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        """Desecrates what will happen after closing the window"""
        self.destroy()
        home = home_window.HomeWindow(self.username)
        home.mainloop()

    def see_details(self, exp_id):
        """Shows details of a specific expense"""
        self.destroy()
        exp_detail = ExpenseDetail(exp_id, self.username)
        exp_detail.mainloop()

    def add_new_expense(self):
        """Adds new expense for logged user"""
        self.destroy()
        add_exp = AddExpense(get_user_name(self.username)[0])
        add_exp.mainloop()
    
    def refresh(self, category):
        """Refresh the list of all expenses that are owned by logged user"""
        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        query = self.filter_data(category)

        db = database_connect.DatabaseConnector()

        expenses = db.select_data(query)
        for idx, expense in enumerate(expenses):
            expanse_name = customtkinter.CTkLabel(master=self.frame, text=textwrap.shorten(expense[0], width=25,
                                                                                           placeholder='...'),
                                                  font=("Arial", 24, "normal"))
            expanse_name.grid(pady=20, padx=10, row=idx, column=0)
            
            category_label = customtkinter.CTkLabel(master=self.frame, text=expense[4], font=("Arial", 24, "normal"))
            category_label.grid(pady=20, padx=10, row=idx, column=1)
            
            date = customtkinter.CTkLabel(master=self.frame, text=str(expense[2]).split(' ')[0],
                                          font=("Arial", 24, "normal"))
            date.grid(pady=20, padx=10, row=idx, column=2)

            price = customtkinter.CTkLabel(master=self.frame, text=expense[3], font=("Arial", 24, "normal"))
            price.grid(pady=20, padx=10, row=idx, column=3)
            
            exp_id = expense[5]

            detail_button = customtkinter.CTkButton(master=self.frame, text="Detail",
                                                    command=lambda exp_id=exp_id: self.see_details
                                                    (exp_id), font=('Arial', 24, 'normal'))
            detail_button.grid(pady=20, padx=10, row=idx, column=4)

    def filter_data(self, category):
        """Applies a filter on a list"""
        name = self.expense_name_entry.get()
        choosed_filter = self.filter_opt.get()

        if filter == 'Amount descending':
            sort_filter = 'expenses.amount DESC'
        elif filter == 'Amount ascending':
            sort_filter = 'expenses.amount ASC'
        elif filter == 'Date descending':
            sort_filter = 'expenses.add_date DESC'
        else:
            sort_filter = 'expenses.add_date ASC'

        if category == 'All':
            category_filter = ''
        else:
             category_filter = f"AND categories.name = '{category}'"

        query = f"SELECT expenses.name, expenses.description, expenses.add_date, expenses.amount, categories.name, " \
                f"expenses.id FROM expenses JOIN categories ON expenses.category_id=categories.id WHERE " \
                f"expenses.user_id={get_user_name(self.username)[0]} {category_filter} AND expenses.name LIKE " \
                f"'%{name}%' ORDER BY {sort_filter}"

        return query

    def download_data(self, category):
        """Allows to download all data of a given user"""
        db = database_connect.DatabaseConnector()
        query = self.filter_data(category)
        expenses = list(db.select_data(query))
        for idx, exp in enumerate(expenses):
            expenses[idx] = list(exp[:-1])
            for i, e in enumerate(exp):
                if isinstance(e, str):
                    expenses[idx][i] = e.replace('\n', '\\n')
        headers = ['Name', 'Description', 'Add_date', 'Amount', 'Category']

        if self.format_type.get() == 'csv':
            with open('expenses.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(expenses)
        else:
            expenses_with_headers = []
            for exp in expenses:
                exp_dict = {headers[i]: exp[i] for i in range(len(headers))}
                expenses_with_headers.append(exp_dict)

            with open('expenses.json', 'w') as f:
                json.dump(expenses_with_headers, f, default=str, indent=4)
