import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar, DateEntry

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class GenerateReport(customtkinter.CTk):
    def __init__(self, username, summary, currency, number):
        self.username = username
        self.summary = summary
        self.currency = currency
        self.number = number
        super().__init__()
        self.geometry("1600x675")
        self.title("Summary")
        self.frame = customtkinter.CTkFrame(master=self, width=1300, height=500)
        self.frame.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)       
        self.resizable(False, False)
        self.window_flag = 1

        self.title = customtkinter.CTkLabel(master=self, text='Day summary', font=('Arial', 35, 'normal'))
        self.title.place(relx=0.4, rely=0.05)

        #input date

        self.day_entry = customtkinter.CTkEntry(master=self.frame,width=300, placeholder_text='01-01-2020', font=("Arial", 30, "normal"))
        self.day_entry.grid(pady=18, padx=25, row=0, column=0,  sticky='nsew')

        self.generate_daily = customtkinter.CTkButton(master=self.frame, text="Generate daily report", 
                                                      font=("Arial", 26, "normal"),
                                                     command=lambda: show_daily(self.username))
        self.generate_daily.grid(pady=18, padx=10, row=0, column=1, sticky="w")

        self.total = customtkinter.CTkLabel(master=self.frame, text='Total:', font=("Arial", 25, "normal"))
        self.total.grid(pady=18, padx=10, row=1, column=0, sticky='w')

        self.total_amount = customtkinter.CTkLabel(master=self.frame, text=f"{str(round(sum(summary.values()), 2))} {currency}", font=("Arial", 25, "normal"))
        self.total_amount.grid(pady=18, padx=10, row=1, column=1, sticky='e')

        self.number_of_exp = customtkinter.CTkLabel(master=self.frame, text='Number of expenses:', font=("Arial", 25, "normal"),
                                           wraplength=700)
        self.number_of_exp.grid(pady=18, padx=10, row=2, column=0, sticky='w')

        self.number = customtkinter.CTkLabel(master=self.frame, text=self.number, font=("Arial", 25, "normal"))
        self.number.grid(pady=18, padx=10, row=2, column=1, sticky='e')
       
        self.entertainment = customtkinter.CTkLabel(master=self.frame, text="Entertainment", font=("Arial", 25, "normal"))
        self.entertainment.grid(row=3, column=0, padx=10, pady=20, sticky='w')

        self.total_entertainment = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Entertainment']} {currency}", font=("Arial", 25, "normal"))
        self.total_entertainment.grid(row=3, column=1, padx=10, pady=20, sticky='e')

        self.shopping = customtkinter.CTkLabel(master=self.frame, text="Shopping", font=("Arial", 25, "normal"))
        self.shopping.grid(row=4, column=0, padx=10, pady=20, sticky='w')

        self.total_shopping = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Shopping']} {currency}", font=("Arial", 25, "normal"))
        self.total_shopping.grid(row=4, column=1, padx=10, pady=20, sticky='e')

        self.bills = customtkinter.CTkLabel(master=self.frame, text="Bills", font=("Arial", 25, "normal"))
        self.bills.grid(row=5, column=0, padx=10, pady=20, sticky='w')

        self.total_bills = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Bills']} {currency}", font=("Arial", 25, "normal"))
        self.total_bills.grid(row=5, column=1, padx=10, pady=20, sticky='e')

        self.subscriptions = customtkinter.CTkLabel(master=self.frame, text="Subscriptions", font=("Arial", 25, "normal"))
        self.subscriptions.grid(row=6, column=0, padx=10, pady=20, sticky='w')

        self.total_subscriptions = customtkinter.CTkLabel(master=self.frame, text=f"{str(summary['Subscriptions'])} {currency}", font=("Arial", 25, "normal"))
        self.total_subscriptions.grid(row=6, column=1, padx=10, pady=20, sticky='e')

        self.other = customtkinter.CTkLabel(master=self.frame, text="Other", font=("Arial", 25, "normal"))
        self.other.grid(row=7, column=0, padx=10, pady=20, sticky='w')

        self.total_other = customtkinter.CTkLabel(master=self.frame, text=f"{str(summary['Other'])} {currency}", font=("Arial", 25, "normal"))
        self.total_other.grid(row=7, column=1, padx=10, pady=20, sticky='e')


        # monthly summary -----------------------------------------


        self.title2 = customtkinter.CTkLabel(master=self, text='Month summary', font=('Arial', 35, 'normal'))
        self.title2.place(relx=0.4, rely=0.05)

        #input date
        self.day_entry2 = customtkinter.CTkEntry(master=self.frame,width=300, placeholder_text='01-2020', font=("Arial", 30, "normal"))
        self.day_entry2.grid(pady=18, padx=25, row=0, column=2,  sticky='nsew')

        self.generate_monthly = customtkinter.CTkButton(master=self.frame, text="Generate daily report", 
                                                      font=("Arial", 26, "normal"),
                                                     command=lambda: show_monthly(self.username))
        self.generate_monthly.grid(pady=18, padx=10, row=0, column=3, sticky="w")

        self.total2 = customtkinter.CTkLabel(master=self.frame, text='Total:', font=("Arial", 25, "normal"))
        self.total2.grid(pady=18, padx=10, row=1, column=2, sticky='w')

        self.total_amount2 = customtkinter.CTkLabel(master=self.frame, text=f"{str(round(sum(summary.values()), 2))} {currency}",
                                                   font=("Arial", 25, "normal"))
        self.total_amount2.grid(pady=18, padx=10, row=1, column=3, sticky='e')

        self.number_of_exp2 = customtkinter.CTkLabel(master=self.frame, text='Number of expenses:',
                                                    font=("Arial", 25, "normal"),
                                                    wraplength=700)
        self.number_of_exp2.grid(pady=18, padx=10, row=2, column=2, sticky='w')

        self.number2 = customtkinter.CTkLabel(master=self.frame, text=self.number, font=("Arial", 25, "normal"))
        self.number2.grid(pady=18, padx=10, row=2, column=3, sticky='e')

        self.entertainment2 = customtkinter.CTkLabel(master=self.frame, text="Entertainment",
                                                    font=("Arial", 25, "normal"))
        self.entertainment2.grid(row=3, column=2, padx=10, pady=20, sticky='w')

        self.total_entertainment2 = customtkinter.CTkLabel(master=self.frame,
                                                          text=f"{summary['Entertainment']} {currency}",
                                                          font=("Arial", 25, "normal"))
        self.total_entertainment2.grid(row=3, column=3, padx=10, pady=20, sticky='e')

        self.shopping2 = customtkinter.CTkLabel(master=self.frame, text="Shopping", font=("Arial", 25, "normal"))
        self.shopping2.grid(row=4, column=2, padx=10, pady=20, sticky='w')

        self.total_shopping2= customtkinter.CTkLabel(master=self.frame, text=f"{summary['Shopping']} {currency}",
                                                     font=("Arial", 25, "normal"))
        self.total_shopping2.grid(row=4, column=3, padx=10, pady=20, sticky='e')

        self.bills2 = customtkinter.CTkLabel(master=self.frame, text="Bills", font=("Arial", 25, "normal"))
        self.bills2.grid(row=5, column=2, padx=10, pady=20, sticky='w')

        self.total_bills2 = customtkinter.CTkLabel(master=self.frame, text=f"{summary['Bills']} {currency}",
                                                  font=("Arial", 25, "normal"))
        self.total_bills2.grid(row=5, column=3, padx=10, pady=20, sticky='e')

        self.subscriptions2 = customtkinter.CTkLabel(master=self.frame, text="Subscriptions",
                                                    font=("Arial", 25, "normal"))
        self.subscriptions2.grid(row=6, column=2, padx=10, pady=20, sticky='w')

        self.total_subscriptions2 = customtkinter.CTkLabel(master=self.frame,
                                                          text=f"{str(summary['Subscriptions'])} {currency}",
                                                          font=("Arial", 25, "normal"))
        self.total_subscriptions2.grid(row=6, column=3, padx=10, pady=20, sticky='e')

        self.other2 = customtkinter.CTkLabel(master=self.frame, text="Other", font=("Arial", 25, "normal"))
        self.other2.grid(row=7, column=2, padx=10, pady=20, sticky='w')

        self.total_other2 = customtkinter.CTkLabel(master=self.frame, text=f"{str(summary['Other'])} {currency}",
                                                  font=("Arial", 25, "normal"))
        self.total_other2.grid(row=7, column=3, padx=10, pady=20, sticky='e')




        def show_daily( username):  
            username=username
            day=self.day_entry.get()
            db = database_connect.DatabaseConnector()
            query = f"SELECT e.amount, c.name from expenses AS e JOIN users AS u ON e.user_id=u.id JOIN categories AS " \
                    f"c ON e.category_id=c.id WHERE u.username='{username}'AND e.add_date={day}"
            results = db.select_data(query)

            summary = {'Entertainment': 0, 'Shopping': 0, 'Bills': 0, 'Subscriptions': 0, 'Other': 0}
            for r in results:
                if r[1] == 'Entertainment':
                    summary['Entertainment'] += float(r[0])
                elif r[1] == 'Shopping':
                    summary['Shopping'] += float(r[0])
                elif r[1] == 'Bills':
                    summary['Bills'] += float(r[0])
                elif r[1] == 'Subscriptions':
                    summary['Subscriptions'] += float(r[0])
                else:
                    summary['Other'] += float(r[0])

        
            query = f"SELECT currency FROM users WHERE username='{username}'"
            self.currency = db.select_data(query, 'one')[0]

        #funkcja testowa
        def show_daily2(self,username):
            db = database_connect.DatabaseConnector()
            query = f"SELECT e.amount, c.name from expenses AS e JOIN users AS u ON e.user_id=u.id JOIN categories AS " \
                f"c ON e.category_id=c.id WHERE u.username='{self.username}'AND e.add_date=CURRENT_DATE"
            self.results = db.select_data(query)

            self.summary = {'Entertainment': 0, 'Shopping': 0, 'Bills': 0, 'Subscriptions': 0, 'Other': 0}
            for r in self.results:
                if r[1] == 'Entertainment':
                    self.summary['Entertainment'] += float(r[0])
                elif r[1] == 'Shopping':
                    self.summary['Shopping'] += float(r[0])
                elif r[1] == 'Bills':
                    self.summary['Bills'] += float(r[0])
                elif r[1] == 'Subscriptions':
                    self.summary['Subscriptions'] += float(r[0])
                else:
                    self.summary['Other'] += float(r[0])

        
            query = f"SELECT currency FROM users WHERE username='{self.username}'"
            self.currency = db.select_data(query, 'one')[0]

            self.spending_summary = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)),
                                                        height=270, fg_color="#242424")
            self.spending_summary.grid(column=1, row=2, sticky="w")
            self.spending_summary.grid_columnconfigure((0, 1), weight=1)
            self.spending_summary.grid_rowconfigure((0, 1), weight=1)
            self.total = customtkinter.CTkLabel(master=self.spending_summary,
                                                text=f"Daily total: {str(round(sum(self.summary.values()), 2))} "
                                                    f"{self.currency}", font=("Arial", 30, "normal"))
            self.total.grid(pady=18, padx=10, column=0, row=0)

            self.view = customtkinter.CTkButton(master=self.spending_summary, text='View details',
                                                command=self.see_details, font=('Arial', 30, 'normal'))
            self.view.grid(pady=18, padx=10, column=1, row=0)

            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            query = f"SELECT e.amount, c.name, EXTRACT(MONTH FROM add_date) from expenses AS e JOIN " \
                    f"users AS u ON e.user_id=u.id JOIN categories AS c ON e.category_id=c.id " \
                    f"WHERE u.username='{self.username}' AND EXTRACT(MONTH FROM add_date) = {current_month} " \
                    f"AND EXTRACT(YEAR FROM add_date) = {current_year}"
            self.month_results = db.select_data(query)
            self.month_summary = {'Entertainment': 0, 'Shopping': 0, 'Bills': 0, 'Subscriptions': 0, 'Other': 0}
            for r in self.month_results:
                if r[1] == 'Entertainment':
                    self.month_summary['Entertainment'] += float(r[0])
                elif r[1] == 'Shopping':
                    self.month_summary['Shopping'] += float(r[0])
                elif r[1] == 'Bills':
                    self.month_summary['Bills'] += float(r[0])
                elif r[1] == 'Subscriptions':
                    self.month_summary['Subscriptions'] += float(r[0])
                else:
                    self.month_summary['Other'] += float(r[0])

            query = f"SELECT currency FROM users WHERE username='{self.username}'"
            self.currency = db.select_data(query, 'one')[0]
            self.month_total = customtkinter.CTkLabel(master=self.spending_summary,
                                                    text=f"Month total: {str(round(sum(self.month_summary.values()), 2))} "
                                                        f"{self.currency}", font=("Arial", 30, "normal"))
            self.month_total.grid(pady=18, padx=10, column=0, row=1)


        def show_monthly(self, username):
            pass

        