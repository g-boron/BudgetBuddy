import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.budget import Budget
from tkcalendar import Calendar
from tkinter import ttk
from modules import all_revenues


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class EditRevenue(customtkinter.CTk):
    def __init__(self, revenue_id, user_id):
        self.id_rev = revenue_id
        self.id_user = user_id
        super().__init__()
        self.geometry("800x800")
        self.title("Edit your revenue")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.window_flag = 1

        records = self.get_previous(self.id_rev)

        previous_date = str(records[4])
        print(previous_date)
        previous_year = int(previous_date[:4])
        previous_month = int(previous_date[5:7])
        previous_day = int(previous_date[8:10])

        self.label = customtkinter.CTkLabel(master=self.frame, text="Edit this revenue", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

        self.name_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text=f"Name", justify=CENTER)
        self.name_entry.insert(0, records[1])
        self.name_entry.grid(pady=20, padx=10, row=1, column=0, sticky="ew", columnspan=2)

        self.desc_text = customtkinter.CTkTextbox(master=self.frame, width=200, fg_color='#343638',
                                                  border_color='#565b5e', border_width=2, text_color='#8e9e8f')
        self.desc_text.grid(pady=10, padx=10, row=2, column=0, sticky='ew', columnspan=2)
        self.desc_text.insert(1.0, records[2])

        # calendar
        style = ttk.Style(self)
        style.theme_use('clam')
        self.cal = Calendar(self.frame, selectmode='day', year=previous_year, month=previous_month, day=previous_day,
                            font='Arial 12', background="#242424",
                            disabledbackground="black", bordercolor="black",
                            headersbackground="black", normalbackground="black", foreground='white',
                            normalforeground='white', headersforeground='white', selectbackground='#1f6aa5')
        self.cal.grid(column=0, row=3, pady=35, padx=15, columnspan=2)

        self.amount_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text=f'Amount', justify=CENTER)
        self.amount_entry.insert(0, records[3])
        self.amount_entry.grid(pady=10, padx=10, row=4, column=0, sticky='ew', columnspan=2)

        db = database_connect.DatabaseConnector()
        query = 'SELECT name FROM categories'
        results = db.select_data(query)

        self.delete = customtkinter.CTkButton(master=self.frame, text="Cancel", font=("Arial", 12, "normal"),
                                              command=lambda: self.destroy())
        self.delete.grid(row=6, column=0, padx=10, pady=20, sticky='sw')

        self.edit = customtkinter.CTkButton(master=self.frame, text="Confirm", font=("Arial", 12, "normal"),
                                            command=lambda revenue_id=revenue_id: self.make_changes(revenue_id))
        self.edit.grid(row=6, column=1, padx=10, pady=20, sticky='sw')

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        self.destroy()
        db = database_connect.DatabaseConnector()
        query = f"SELECT username FROM users WHERE id={self.id_user}"
        username = db.select_data(query, 'one')[0]
        revenues = all_revenues.AllRevenues(username)
        revenues.mainloop()

    def get_previous(self, revenue_id):
        db = database_connect.DatabaseConnector()
        query = f"SELECT id, name, description, amount, add_date, user_id FROM revenues WHERE id = '{revenue_id}'"
        exp = db.select_data(query, 'one')
        return exp

    def make_changes(self, revenue_id):
        rev_id = revenue_id
        new_name = self.name_entry.get()
        new_description = self.desc_text.get("1.0", END)
        new_day = self.cal.selection_get().strftime('%Y-%m-%d')
        new_amount = self.amount_entry.get()
        records = self.get_previous(rev_id)

        if new_name != '' and self.isfloat(new_amount) and float(new_amount) > 0:
            budget = Budget(records[5])
            check = budget.edit_revenue(new_name, new_description, float(new_amount), new_day, revenue_id)
            if check:
                messagebox.showinfo('Success', 'You successfully changed one revenue!')
                self.on_closing()
            else:
                messagebox.showerror('Error', 'You do not have enough money!')
        else:
            messagebox.showerror('Error', 'Please enter valid data.')

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
