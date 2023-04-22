import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from modules.expense_detail import ExpenseDetail
from modules.add_expense import AddExpense
import textwrap

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
        '''
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)'''
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

        self.frame = customtkinter.CTkScrollableFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.refresh('All')

        self.addbtn = customtkinter.CTkButton(master=self, text='Add new expense', command=self.add_new_expense,
                                              font=('Arial', 30, 'normal'))
        self.addbtn.place(relx=0.2, rely=0.9, anchor='center')

        self.refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=lambda: self.refresh(str(self.category_opt.get())),
                                              font=('Arial', 30, 'normal'))
        self.refreshbtn.place(relx=0.5, rely=0.9, anchor='center')

        self.exitbtn = customtkinter.CTkButton(master=self, text='Exit', command=lambda: self.destroy(),
                                              font=('Arial', 30, 'normal'))
        self.exitbtn.place(relx=0.8, rely=0.9, anchor='center')

    def see_details(self, exp_id, user_login):
        self.destroy()
        exp_detail = ExpenseDetail(exp_id, self.get_user_name(user_login)[1])
        exp_detail.mainloop()

    def add_new_expense(self):
        self.destroy()
        add_exp = AddExpense(self.get_user_name(self.username)[0])
        add_exp.mainloop()
    
    def refresh(self, category):
        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        db = database_connect.DatabaseConnector()
        if category == 'All':
            query = f"SELECT expenses.name, expenses.description, expenses.add_date, expenses.amount, categories.name, " \
                    f"expenses.id FROM expenses JOIN categories ON expenses.category_id=categories.id WHERE " \
                    f"expenses.user_id={self.get_user_name(self.username)[0]}"
        else:
            query = f"SELECT expenses.name, expenses.description, expenses.add_date, expenses.amount, categories.name, " \
                    f"expenses.id FROM expenses JOIN categories ON expenses.category_id=categories.id WHERE " \
                    f"expenses.user_id={self.get_user_name(self.username)[0]} AND categories.name='{category}'"
            print(query)

        expenses = db.select_data(query)
        for idx, expense in enumerate(expenses):
            self.expname = customtkinter.CTkLabel(master=self.frame, text=textwrap.shorten(expense[0], width=25,
                                                                                           placeholder='...'),
                                                  font=("Arial", 24, "normal"))
            self.expname.grid(pady=20, padx=10, row=idx, column=0)
            
            self.category = customtkinter.CTkLabel(master=self.frame, text=expense[4], font=("Arial", 24, "normal"))
            self.category.grid(pady=20, padx=10, row=idx, column=1)
            
            self.date = customtkinter.CTkLabel(master=self.frame, text=str(expense[2]).split(' ')[0], font=("Arial", 24, "normal"))
            self.date.grid(pady=20, padx=10, row=idx, column=2)
            
            exp_id = expense[5]

            self.detailbtn = customtkinter.CTkButton(master=self.frame, text="Detail",
                                                     command=lambda exp_id=exp_id: self.see_details(exp_id, self.username),
                                                     font=('Arial', 24, 'normal'))
            self.detailbtn.grid(pady=20, padx=10, row=idx, column=3)

    def get_user_name(self, user_login):
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT id, name FROM users WHERE username='{user_login}';"
        user_name = db.select_data(name_query, 'one')
        return user_name
