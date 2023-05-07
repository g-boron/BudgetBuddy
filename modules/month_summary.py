import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from datetime import datetime

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class MonthSummary(customtkinter.CTk):
    def __init__(self, username, summary, currency, number):
        self.username = username
        self.summary = summary
        self.currency = currency
        self.number = number
        super().__init__()
        self.geometry("800x675")
        self.title("Month summary")
        self.frame = customtkinter.CTkFrame(master=self, width=650, height=500)
        self.frame.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.resizable(False, False)
        self.window_flag = 1

        self.title = customtkinter.CTkLabel(master=self, text='Month summary', font=('Arial', 35, 'normal'))
        self.title.place(relx=0.4, rely=0.05)

        self.date = customtkinter.CTkLabel(master=self.frame, text=datetime.today().strftime('%m-%Y'),
                                           font=("Arial", 30, "normal"))
        self.date.grid(pady=18, padx=250, row=0, column=0, columnspan=2, sticky='nsew')

        self.total = customtkinter.CTkLabel(master=self.frame, text='Total:', font=("Arial", 25, "normal"))
        self.total.grid(pady=18, padx=10, row=1, column=0, sticky='w')

        self.total_amount = customtkinter.CTkLabel(master=self.frame, text=f"{str(sum(summary.values()))} {currency}",
                                                   font=("Arial", 25, "normal"))
        self.total_amount.grid(pady=18, padx=10, row=1, column=1, sticky='e')

        self.number_of_exp = customtkinter.CTkLabel(master=self.frame, text='Number of expenses:',
                                                    font=("Arial", 25, "normal"),
                                                    wraplength=700)
        self.number_of_exp.grid(pady=18, padx=10, row=2, column=0, sticky='w')

        self.number = customtkinter.CTkLabel(master=self.frame, text=self.number, font=("Arial", 25, "normal"))
        self.number.grid(pady=18, padx=10, row=2, column=1, sticky='e')

        self.entertainment = customtkinter.CTkLabel(master=self.frame, text="Entertainment",
                                                    font=("Arial", 25, "normal"))
        self.entertainment.grid(row=3, column=0, padx=10, pady=20, sticky='w')

        self.total_entertainment = customtkinter.CTkLabel(master=self.frame,
                                                          text=f"{summary['Entertainment']} {currency}",
                                                          font=("Arial", 25, "normal"))
        self.total_entertainment.grid(row=3, column=1, padx=10, pady=20, sticky='e')

        self.shopping = customtkinter.CTkLabel(master=self.frame, text="Shopping", font=("Arial", 25, "normal"))
        self.shopping.grid(row=4, column=0, padx=10, pady=20, sticky='w')

        self.total_shopping = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Shopping']} {currency}",
                                                     font=("Arial", 25, "normal"))
        self.total_shopping.grid(row=4, column=1, padx=10, pady=20, sticky='e')

        self.bills = customtkinter.CTkLabel(master=self.frame, text="Bills", font=("Arial", 25, "normal"))
        self.bills.grid(row=5, column=0, padx=10, pady=20, sticky='w')

        self.total_bills = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Bills']} {currency}",
                                                  font=("Arial", 25, "normal"))
        self.total_bills.grid(row=5, column=1, padx=10, pady=20, sticky='e')

        self.subscriptions = customtkinter.CTkLabel(master=self.frame, text="Subscriptions",
                                                    font=("Arial", 25, "normal"))
        self.subscriptions.grid(row=6, column=0, padx=10, pady=20, sticky='w')

        self.total_subscriptions = customtkinter.CTkLabel(master=self.frame,
                                                          text=f"{str(summary['Subscriptions'])} {currency}",
                                                          font=("Arial", 25, "normal"))
        self.total_subscriptions.grid(row=6, column=1, padx=10, pady=20, sticky='e')

        self.other = customtkinter.CTkLabel(master=self.frame, text="Other", font=("Arial", 25, "normal"))
        self.other.grid(row=7, column=0, padx=10, pady=20, sticky='w')

        self.total_other = customtkinter.CTkLabel(master=self.frame, text=f"{str(summary['Other'])} {currency}",
                                                  font=("Arial", 25, "normal"))
        self.total_other.grid(row=7, column=1, padx=10, pady=20, sticky='e')
