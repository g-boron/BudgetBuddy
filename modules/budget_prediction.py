import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from tkinter import messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta
from modules.functions.prediction import Predictor


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class BudgetPrediction(customtkinter.CTk):
    def __init__(self, user_id, currency):
        self.user_id = user_id
        self.currency = currency
        super().__init__()
        self.geometry("800x600")
        self.title("Budget prediction")
        self.frame = customtkinter.CTkFrame(master=self, width=700, height=550)
        self.frame.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.window_flag = 1

        predictor = Predictor(self.user_id)
        data = predictor.predict_budget()

        self.title = customtkinter.CTkLabel(master=self, text='Budget prediction', font=('Arial', 35, 'normal'))
        self.title.place(relx=0.4, rely=0.05)

        self.date = customtkinter.CTkLabel(master=self.frame, text=(datetime.today() + relativedelta(months=1)).strftime('%m-%Y'),
                                           font=("Arial", 30, "normal"))
        self.date.grid(pady=18, padx=250, row=0, column=0, columnspan=2, sticky='nsew')

        self.total = customtkinter.CTkLabel(master=self.frame, text='Total:', font=("Arial", 25, "normal"))
        self.total.grid(pady=18, padx=10, row=1, column=0, sticky='w')

        self.total_amount = customtkinter.CTkLabel(master=self.frame, text=f"{round(data['Total'], 2)} {self.currency}",
                                                   font=("Arial", 25, "normal"))
        self.total_amount.grid(pady=18, padx=10, row=1, column=1, sticky='e')

        self.entertainment = customtkinter.CTkLabel(master=self.frame, text="Entertainment",
                                                    font=("Arial", 25, "normal"))
        self.entertainment.grid(row=2, column=0, padx=10, pady=20, sticky='w')

        self.total_entertainment = customtkinter.CTkLabel(master=self.frame,
                                                          text=f"{round(data['Entertainment'], 2)} {self.currency}",
                                                          font=("Arial", 25, "normal"))
        self.total_entertainment.grid(row=2, column=1, padx=10, pady=20, sticky='e')

        self.shopping = customtkinter.CTkLabel(master=self.frame, text="Shopping", font=("Arial", 25, "normal"))
        self.shopping.grid(row=3, column=0, padx=10, pady=20, sticky='w')

        self.total_shopping = customtkinter.CTkLabel(master=self.frame, text=f"{round(data['Shopping'], 2)} {self.currency}",
                                                     font=("Arial", 25, "normal"))
        self.total_shopping.grid(row=3, column=1, padx=10, pady=20, sticky='e')

        self.bills = customtkinter.CTkLabel(master=self.frame, text="Bills", font=("Arial", 25, "normal"))
        self.bills.grid(row=4, column=0, padx=10, pady=20, sticky='w')

        self.total_bills = customtkinter.CTkLabel(master=self.frame, text=f"{round(data['Bills'], 2)} {self.currency}",
                                                  font=("Arial", 25, "normal"))
        self.total_bills.grid(row=4, column=1, padx=10, pady=20, sticky='e')

        self.subscriptions = customtkinter.CTkLabel(master=self.frame, text="Subscriptions",
                                                    font=("Arial", 25, "normal"))
        self.subscriptions.grid(row=5, column=0, padx=10, pady=20, sticky='w')

        self.total_subscriptions = customtkinter.CTkLabel(master=self.frame,
                                                          text=f"{round(data['Subscriptions'], 2)} {self.currency}",
                                                          font=("Arial", 25, "normal"))
        self.total_subscriptions.grid(row=5, column=1, padx=10, pady=20, sticky='e')

        self.other = customtkinter.CTkLabel(master=self.frame, text="Other", font=("Arial", 25, "normal"))
        self.other.grid(row=6, column=0, padx=10, pady=20, sticky='w')

        self.total_other = customtkinter.CTkLabel(master=self.frame, text=f"{round(data['Other'], 2)} {self.currency}",
                                                  font=("Arial", 25, "normal"))
        self.total_other.grid(row=6, column=1, padx=10, pady=20, sticky='e')
