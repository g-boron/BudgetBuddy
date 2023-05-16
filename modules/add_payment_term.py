import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import ttk
from modules import payment_term
from modules.functions.get_user_name import *
from modules.functions.get_user_id import *


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


class AddPaymentData(customtkinter.CTk):
    def __int__(self, user_login):
        super().__init__()
        self.login = user_login
        self.geometry("800x800")
        self.title("Add new payment term")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.resizable(False, False)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Add new payment term", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10)

        self.name_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Name", justify=CENTER)
        self.name_entry.grid(pady=20, padx=10, row=1, column=0, sticky="ew")
        # calendar
        style = ttk.Style(self)
        style.theme_use('clam')
        self.cal = Calendar(self.frame, selectmode='day', font='Arial 12', background="#242424",
                            disabledbackground="black", bordercolor="black",
                            headersbackground="black", normalbackground="black", foreground='white',
                            normalforeground='white', headersforeground='white', selectbackground='#1f6aa5')
        self.cal.grid(column=0, row=2, pady=35, padx=15)

        db = database_connect.DatabaseConnector()
        query = f'SELECT currency FROM users WHERE id = {get_user_id(self.login)}'
        currency = db.select_data(query, 'one')[0]

        self.amount_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text=f'Amount [{currency}]',
                                                   justify=CENTER)
        self.amount_entry.grid(pady=10, padx=10, row=3, column=0, sticky='ew')

        self.add_button = customtkinter.CTkButton(master=self.frame, text='Add new payment term',
                                                  command=self.add_new_payment_term, font=('Arial', 25, 'normal'))
        self.add_button.grid(padx=20, pady=10, row=4, column=0, sticky='ew')

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        self.destroy()
        payment_terms = payment_term.PaymentTerm(self.login)
        payment_terms.mainloop()

    def add_new_payment_term(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        day = self.cal.selection_get().strftime('%Y-%m-%d')

        if name != '' and self.isfloat(amount) and float(amount) > 0:
            db = database_connect.DatabaseConnector()
            query = f"INSERT INTO payment_term VALUES({name}, {day}, {amount});"
            messagebox.showinfo('Success', 'You successfully added new payment term!')
            self.on_closing()
        else:
            messagebox.showerror("Error", "Please enter valid data.")

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
