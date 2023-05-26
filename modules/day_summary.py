import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from datetime import datetime
from .functions.summaries import get_daily_summary, get_user_currency


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class DaySummary(customtkinter.CTk):
    def __init__(self, username, number):
        self.username = username
        self.number = number
        super().__init__()
        self.geometry("800x675")
        self.title("Day summary")
        self.frame = customtkinter.CTkFrame(master=self, width=650, height=500)
        self.frame.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.frame.grid_columnconfigure((0, 1), weight=1)       
        self.resizable(False, False)
        self.window_flag = 1

        self.title = customtkinter.CTkLabel(master=self, text='Day summary', font=('Arial', 35, 'normal'))
        self.title.place(relx=0.4, rely=0.025)

        self.choose = customtkinter.CTkEntry(master=self, placeholder_text='Day', font=('Arial', 25,'normal'))
        self.choose.place(relx=0.3, rely=0.1)

        self.btn = customtkinter.CTkButton(master=self, text='Choose', font=('Arial', 25, 'normal'),
                                           command=self.change)
        self.btn.place(relx=0.5, rely=0.1)

        self.refresh('now')
    
    def refresh(self, day):
        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        if day == 'now':
            summary, results = get_daily_summary(self.username)
        else:
            summary, results = get_daily_summary(self.username, day)

        currency = get_user_currency(self.username)

        if day == 'now':
            date = customtkinter.CTkLabel(master=self.frame, text=datetime.today().strftime('%d-%m-%Y'),
                                          font=("Arial", 30, "normal"))
        else:
            date = customtkinter.CTkLabel(master=self.frame, text=day, font=("Arial", 30, "normal"))
        
        date.grid(pady=18, padx=250, row=0, column=0, columnspan=2, sticky='nsew')

        total = customtkinter.CTkLabel(master=self.frame, text='Total:', font=("Arial", 25, "normal"))
        total.grid(pady=18, padx=10, row=1, column=0, sticky='w')

        total_amount = customtkinter.CTkLabel(master=self.frame, text=f"{str(round(sum(summary.values()), 2))} "
                                                                      f"{currency}", font=("Arial", 25, "normal"))
        total_amount.grid(pady=18, padx=10, row=1, column=1, sticky='e')

        number_of_expenses = customtkinter.CTkLabel(master=self.frame, text='Number of expenses:',
                                                    font=("Arial", 25, "normal"), wraplength=700)
        number_of_expenses.grid(pady=18, padx=10, row=2, column=0, sticky='w')

        number = customtkinter.CTkLabel(master=self.frame, text=len(self.results), font=("Arial", 25, "normal"))
        number.grid(pady=18, padx=10, row=2, column=1, sticky='e')
       
        entertainment = customtkinter.CTkLabel(master=self.frame, text="Entertainment", font=("Arial", 25, "normal"))
        entertainment.grid(row=3, column=0, padx=10, pady=20, sticky='w')

        total_entertainment = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Entertainment']} {currency}",
                                                     font=("Arial", 25, "normal"))
        total_entertainment.grid(row=3, column=1, padx=10, pady=20, sticky='e')

        shopping = customtkinter.CTkLabel(master=self.frame, text="Shopping", font=("Arial", 25, "normal"))
        shopping.grid(row=4, column=0, padx=10, pady=20, sticky='w')

        total_shopping = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Shopping']} {currency}",
                                                font=("Arial", 25, "normal"))
        total_shopping.grid(row=4, column=1, padx=10, pady=20, sticky='e')

        bills = customtkinter.CTkLabel(master=self.frame, text="Bills", font=("Arial", 25, "normal"))
        bills.grid(row=5, column=0, padx=10, pady=20, sticky='w')

        total_bills = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Bills']} {currency}",
                                             font=("Arial", 25, "normal"))
        total_bills.grid(row=5, column=1, padx=10, pady=20, sticky='e')

        subscriptions = customtkinter.CTkLabel(master=self.frame, text="Subscriptions", font=("Arial", 25, "normal"))
        subscriptions.grid(row=6, column=0, padx=10, pady=20, sticky='w')

        total_subscriptions = customtkinter.CTkLabel(master=self.frame, text=f"{str(summary['Subscriptions'])} "
                                                                             f"{currency}",
                                                     font=("Arial", 25, "normal"))
        total_subscriptions.grid(row=6, column=1, padx=10, pady=20, sticky='e')

        other = customtkinter.CTkLabel(master=self.frame, text="Other", font=("Arial", 25, "normal"))
        other.grid(row=7, column=0, padx=10, pady=20, sticky='w')

        total_other = customtkinter.CTkLabel(master=self.frame, text=f"{str(summary['Other'])} {currency}",
                                             font=("Arial", 25, "normal"))
        total_other.grid(row=7, column=1, padx=10, pady=20, sticky='e')

    def change(self):
        self.refresh(self.choose.get())
