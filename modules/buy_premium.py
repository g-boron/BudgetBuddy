import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from tkinter import messagebox
from modules.functions.summaries import get_user_currency
from modules.functions.get_users_info import get_user_login
from datetime import datetime, date
from modules.database.database_connect import DatabaseConnector

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class BuyPremium(customtkinter.CTk):
    def __init__(self, user_id):
        self.user_id = user_id
        self.currency = get_user_currency(self.user_id)
        super().__init__()
        self.geometry("800x600")
        self.title("Buy premium")
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

        self.label = customtkinter.CTkLabel(self, text=f'Buy premium, it costs only 15 {self.currency}!\n\n With this price you have summary graphs, \nbudget prediction and budget sharing.', font=('Arial', 35, 'normal'))
        self.label.pack(pady=15)

        self.card_number = customtkinter.CTkEntry(self.frame, placeholder_text='1234 1234 1234 1234', font=('Arial', 25, 'normal'), width=300)
        self.card_number.grid(column=0, row=0, columnspan=3, pady=15, padx=15, sticky='nsew')
        
        self.exp_date_month = customtkinter.CTkEntry(self.frame, placeholder_text='MM', font=('Arial', 25, 'normal'), width=100)
        self.exp_date_month.grid(row=1, column=0, pady=15)

        self.exp_date_year = customtkinter.CTkEntry(self.frame, placeholder_text='YYYY', font=('Arial', 25, 'normal'), width=100)
        self.exp_date_year.grid(row=1, column=1, padx=10)

        self.cvv = customtkinter.CTkEntry(self.frame, placeholder_text='CVV', font=('Arial', 25, 'normal'), width=100)
        self.cvv.grid(row=1, column=3, padx=15)

        self.pay = customtkinter.CTkButton(self.frame, text='Pay', font=('Arial', 30, 'normal'), command=self.check_payment)
        self.pay.grid(row=2, column=1, columnspan=2, pady=15)

    def check_payment(self):
        error = False
        card_number = str(self.card_number.get().replace(' ', ''))
        exp_date = self.exp_date_month.get() + '-' + self.exp_date_year.get()
        expiration_date = datetime.strptime(exp_date, '%m-%Y').date()
        now = date.today()

        if expiration_date < now:
            error = True

        if len(card_number) != 16 or len(self.cvv.get()) != 3:
            error = True

        if error:
            messagebox.showerror('Error', 'Invalid data or expired date!')
        else:
            messagebox.showinfo('Success', 'You are now a premium member!')
            db = DatabaseConnector()
            query = f"UPDATE users SET is_premium=TRUE WHERE username='{self.user_id}'"
            db.make_query(query)
            self.destroy()