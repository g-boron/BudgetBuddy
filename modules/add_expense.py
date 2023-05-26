import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.budget import Budget
from tkcalendar import Calendar
from tkinter import ttk
from modules import all_expenses


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class AddExpense(customtkinter.CTk):
    def __init__(self, user_id):
        self.id = user_id
        super().__init__()
        self.geometry("900x900")
        self.title("Add new expense")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.resizable(False, False)
        self.window_flag = 1

        self.label = customtkinter.CTkLabel(master=self.frame, text="Add new expense", font=("Arial", 35, "normal"))
        self.label.grid(row=0, column=0, padx=20, pady=10)

        self.name_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Name", justify=CENTER)
        self.name_entry.grid(pady=20, padx=10, row=1, column=0, sticky="ew")

        self.desc_text = customtkinter.CTkTextbox(master=self.frame, width=200, fg_color='#343638',
                                                  border_color='#565b5e', border_width=2, text_color='#8e9e8f')
        self.desc_text.grid(pady=10, padx=10, row=2, column=0, sticky='ew')
        self.desc_text.insert(1.0, 'Description')

        # calendar
        style = ttk.Style(self)
        style.theme_use('clam') 
        self.cal = Calendar(self.frame, selectmode='day', font='Arial 12', background="#242424",
                            disabledbackground="black", bordercolor="black",
                            headersbackground="black", normalbackground="black", foreground='white',
                            normalforeground='white', headersforeground='white', selectbackground='#1f6aa5')
        self.cal.grid(column=0, row=3, pady=35, padx=15)

        def on_click(event):
            current_text = self.desc_text.get("1.0", "end-1c")
            if current_text == 'Description':
                self.desc_text.delete("1.0", "end")
                self.desc_text.configure(text_color='#dce4ee')

        self.desc_text.bind("<Button-1>", on_click)

        db = database_connect.DatabaseConnector()
        query = f'SELECT currency FROM users WHERE id = {self.id}'
        currency = db.select_data(query, 'one')[0]

        self.amount_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text=f'Amount [{currency}]',
                                                   justify=CENTER)
        self.amount_entry.grid(pady=10, padx=10, row=4, column=0, sticky='ew')

        query = 'SELECT name FROM categories'
        results = db.select_data(query)
        categories = [r[0] for r in results]

        self.category = customtkinter.CTkOptionMenu(master=self.frame, values=categories)
        self.category.grid(pady=20, padx=10, row=5, column=0, sticky="ew")

        self.add_button = customtkinter.CTkButton(master=self.frame, text='Add new expense',
                                                  command=self.add_new_expense, font=('Arial', 25, 'normal'))
        self.add_button.grid(padx=20, pady=10, row=6, column=0, sticky='ew')

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        self.destroy()
        db = database_connect.DatabaseConnector()
        query = f"SELECT username from users WHERE id = {self.id}"
        username = db.select_data(query, 'one')[0]
        expenses = all_expenses.AllExpenses(username)
        expenses.mainloop()

    def add_new_expense(self):
        name = self.name_entry.get()
        desc = self.desc_text.get("1.0", END)
        amount = self.amount_entry.get()
        day = self.cal.selection_get().strftime('%Y-%m-%d')
        category = str(self.category.get())

        db = database_connect.DatabaseConnector()
        query = f'SELECT spend_limit FROM users WHERE id = {self.id}'
        spend_limit = db.select_data(query, 'one')[0]
        if spend_limit is None:
            spend_limit = 100000000000000
        
        query2 = f"SELECT SUM(amount) FROM expenses WHERE user_id = {self.id} AND EXTRACT(MONTH FROM add_date) = " \
                 f"EXTRACT(MONTH FROM TIMESTAMP '{day}')"
        current_month_revenues = db.select_data(query2, 'one')[0]
        if current_month_revenues is None:
            current_month_revenues = 0

        if float(amount)+float(current_month_revenues) <= float(spend_limit):
            pass
        else:
            messagebox.showerror('Error', f"You exceeded your spend limit this month!, your spend limit is "
                                          f"{spend_limit}, and you already spent {current_month_revenues}")
            return

        if name != '' and self.isfloat(amount) and float(amount) > 0:
            budget = Budget(self.id)
            cat_id = budget.get_category_id(category)
            check = budget.add_expense(name, desc, float(amount), cat_id, day)
            if check:
                messagebox.showinfo('Success', 'You successfully added new expense!')
                self.on_closing()
            else:
                messagebox.showerror('Error', 'You do not have enough money!')
        else:
            messagebox.showerror('Error', 'Please enter valid data.')

        name = self.name_entry.get()
        desc = self.desc_text.get("1.0", END)
        amount = self.amount_entry.get()
        day = self.cal.selection_get().strftime('%Y-%m-%d')

        db = database_connect.DatabaseConnector()
        query = f'SELECT spend_limit FROM users WHERE id = {self.id}'
        spend_limit = db.select_data(query, 'one')[0]
        if spend_limit is None:
            spend_limit = 100000000000000
        
        query2 = f"SELECT SUM(amount) FROM expenses WHERE user_id = {self.id} AND EXTRACT(MONTH FROM add_date) = " \
                 f"EXTRACT(MONTH FROM TIMESTAMP '{day}')"
        current_month_revenues = db.select_data(query2, 'one')[0]
        if current_month_revenues is None:
            current_month_revenues = 0

        if name != '' and self.isfloat(amount):
            if float(amount) + float(current_month_revenues) <= float(spend_limit):
                budget = Budget(self.id)
                budget.add_revenue(name, desc, float(amount), day)
                messagebox.showinfo('Success', 'You successfully added new revenue!')
                self.on_closing()
            else:
                messagebox.showerror("Error", f"You exceeded your spend limit this month!, your spend limit is "
                                              f"{spend_limit}, and you already spent {current_month_revenues}")
               
        else:
            messagebox.showerror("Error", "Please enter valid data.")

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
            