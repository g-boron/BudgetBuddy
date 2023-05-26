from tkinter import *
import customtkinter
from PIL import ImageTk
import modules.home_window
from modules.database import database_connect
from modules.add_payment_term import AddPaymentData
from modules.functions.get_users_info import *
import textwrap
from modules.functions.get_users_info import *
import modules.home_window


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


class PaymentTerm(customtkinter.CTk):
    def __init__(self, username):
        super().__init__()
        self.login = username
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.state('zoomed')
        self.title("Payment term")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.label = customtkinter.CTkLabel(master=self, text=f"{get_user_name(self.login)[1]}'s payment terms",
                                            font=("Arial", 50, "normal"))
        self.label.pack(pady=50)

        self.frame = customtkinter.CTkScrollableFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.name_entry = customtkinter.CTkEntry(master=self, placeholder_text="name", justify=CENTER,
                                                 font=('Arial', 30, 'normal'), width=200)
        self.name_entry.place(x=700, y=150)

        # choose filter option
        self.filter_opt = customtkinter.CTkOptionMenu(self, values=['Date descending', 'Date ascending',
                                                                    'Amount descending', 'Amount ascending'],
                                                      font=('Arial', 30, 'normal'))
        self.filter_opt.place(x=1150, y=150)

        self.refresh()

        self.add_button = customtkinter.CTkButton(master=self, text='Add new payment term',
                                                  command=self.add_new_payment_term, font=('Arial', 30, 'normal'))
        self.add_button.place(relx=0.2, rely=0.9, anchor='center')

        self.refresh_button = customtkinter.CTkButton(master=self, text='Refresh', command=self.refresh,
                                                      font=('Arial', 30, 'normal'))
        self.refresh_button.place(relx=0.5, rely=0.9, anchor='center')

        self.exit_button = customtkinter.CTkButton(master=self, text='Exit', command=self.on_closing,
                                                   font=('Arial', 30, 'normal'))
        self.exit_button.place(relx=0.8, rely=0.9, anchor='center')

    def add_new_payment_term(self):
        self.destroy()
        add_payment_term = AddPaymentData(self.login)
        add_payment_term.mainloop()

    def refresh(self):
        for widget in self.frame.grid_slaves():
            widget.grid_forget()
        db = database_connect.DatabaseConnector()
        name = self.name_entry.get()
        choosed_filter = self.filter_opt.get()

        if filter == 'Amount descending':
            sort_filter = 'amount DESC'
        elif filter == 'Amount ascending':
            sort_filter = 'amount ASC'
        elif filter == 'Date descending':
            sort_filter = 'date DESC'
        else:
            sort_filter = 'date ASC'
        query = f"SELECT name, date, amount, id FROM payment_term " \
                f"WHERE user_id={get_user_id(self.login)} " \
                f"AND name LIKE '%{name}%' ORDER BY {sort_filter}"
        terms = db.select_data(query)
        for idx, terms in enumerate(terms):
            payment_term_name = customtkinter.CTkLabel(master=self.frame, text=textwrap.shorten(terms[0], width=25,
                                                                                                placeholder='...'),
                                                       font=("Arial", 24, "normal"))
            payment_term_name.grid(pady=20, padx=10, row=idx, column=0)

            date = customtkinter.CTkLabel(master=self.frame, text=str(terms[1]).split(' ')[0],
                                          font=("Arial", 24, "normal"))
            date.grid(pady=20, padx=10, row=idx, column=1)

            amount = customtkinter.CTkLabel(master=self.frame, text=terms[2], font=("Arial", 24, "normal"))
            amount.grid(pady=20, padx=10, row=idx, column=2)

    def on_closing(self):
        self.destroy()
        payment_terms = modules.home_window.HomeWindow(self.login)
        payment_terms.mainloop()
