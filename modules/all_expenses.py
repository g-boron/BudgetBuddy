import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from modules.expense_detail import ExpenseDetail
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
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_dark.png")
        self.iconphoto(False, self.iconpath)
        self.resizable(True, True)
        self.label = customtkinter.CTkLabel(master=self, text=f"{self.get_user_name(self.username)[1]}'s expenses",
                                            font=("Arial", 35, "normal"))
        self.label.pack()

        self.frame = customtkinter.CTkScrollableFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        db = database_connect.DatabaseConnector()
        query = f"SELECT expenses.name, expenses.description, expenses.add_date, expenses.amount, categories.name, expenses.id FROM expenses JOIN categories ON expenses.category_id=categories.id WHERE expenses.user_id={self.get_user_name(self.username)[0]}"
        expenses = db.select_data(query)
        for idx, expense in enumerate(expenses):
            self.expname = customtkinter.CTkLabel(master=self.frame, text=textwrap.shorten(expense[0], width=25, placeholder='...'), font=("Arial", 24, "normal"))
            self.expname.grid(pady=20, padx=10, row=idx, column=0)
            
            self.category = customtkinter.CTkLabel(master=self.frame, text=expense[4], font=("Arial", 24, "normal"))
            self.category.grid(pady=20, padx=10, row=idx, column=1)

            self.date = customtkinter.CTkLabel(master=self.frame, text=expense[2], font=("Arial", 24, "normal"))
            self.date.grid(pady=20, padx=10, row=idx, column=2)
            
            exp_id = expense[5]

            self.detailbtn = customtkinter.CTkButton(master=self.frame, text="Detail", command = lambda exp_id=exp_id: self.see_details(exp_id), font=('Arial', 24, 'normal'))
            self.detailbtn.grid(pady=20, padx=10, row=idx, column=3)


    def see_details(self, exp_id):
        exp_detail = ExpenseDetail(exp_id)
        exp_detail.mainloop()


    def get_user_name(self, user_login):
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT id, name FROM users WHERE username='{user_login}';"
        user_name = db.select_data(name_query, 'one')
        return user_name
