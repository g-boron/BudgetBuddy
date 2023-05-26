from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import ttk
from modules import payment_term
from modules.functions.get_users_info import *

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class AddPaymentData(customtkinter.CTk):
    def __init__(self, user_id):
        self.login = user_id
        super().__init__()
        self.geometry("600x700")
        self.title("Add new expense")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.resizable(False, False)

        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Add new payment term",
                                            font=("Arial", 35, "normal"))
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

    def add_new_payment_term(self):
        name = str(self.name_entry.get())
        amount = self.amount_entry.get()
        day = self.cal.selection_get().strftime('%Y-%m-%d')

        if name != '' and self.isfloat(amount) and float(amount) > 0:
            db = database_connect.DatabaseConnector()
            query = f"INSERT INTO payment_term (name, date, amount, user_id) " \
                    f"VALUES('{name}', '{day}', '{amount}', '{get_user_id(self.login)}');"
            db.make_query(query)
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

    def on_closing(self):
        self.destroy()
        payment_terms = payment_term.PaymentTerm(self.login)
        payment_terms.mainloop()
