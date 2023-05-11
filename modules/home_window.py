import datetime
from tkinter import *
from tkinter import ttk
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from modules.all_expenses import AllExpenses
from modules.all_revenues import AllRevenues
from modules.change_password import ChangePassword
from modules.day_summary import DaySummary
from modules.month_summary import MonthSummary
from tkcalendar import Calendar
import os
from modules import login
import matplotlib as mat
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calendar import monthrange
from operator import add


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class HomeWindow(customtkinter.CTk):
    def __init__(self, user_login):
        self.username = user_login
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d" % (screen_width, screen_height))
        self.state('zoomed')
        self.title("BudgetBuddy")
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.resizable(True, True)
        #   -------------------------------- top panel --------------------------------
        self.logo = PhotoImage(file="./images/logo_transparent_small.png")
        self.canvas = Canvas(width=140, height=150, bg="#242424", highlightthickness=0)
        self.canvas.create_image(90, 101, image=self.logo)
        self.canvas.grid(column=0, row=0, padx=0, pady=0, sticky="nw")
        self.label = customtkinter.CTkLabel(master=self, text=f"Welcome, {self.get_user_name(self.username)}",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=30, padx=10, row=0, column=1, sticky="nw")
        #   -------------------------------- left panel --------------------------------
        self.menu_frame = customtkinter.CTkScrollableFrame(master=self, width=int(((screen_width / 3) - 20)),
                                                           height=440)
        self.menu_frame.grid(column=0, row=1, sticky="n")
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.label = customtkinter.CTkLabel(master=self.menu_frame, text="Main menu",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=18, padx=10, row=0, column=0)
        self.expenses = customtkinter.CTkButton(master=self.menu_frame, text="My expenses", fg_color="transparent",
                                                font=("Arial", 26, "normal"), command=self.show_expenses)
        self.expenses.grid(pady=18, padx=10, row=1, column=0, sticky="new")
        self.revenues = customtkinter.CTkButton(master=self.menu_frame, text="My revenues", fg_color="transparent",
                                                font=("Arial", 26, "normal"), command=self.show_revenues)
        self.revenues.grid(pady=18, padx=10, row=2, column=0, sticky="new")
        self.element3 = customtkinter.CTkButton(master=self.menu_frame, text="element4", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element3.grid(pady=18, padx=10, row=4, column=0, sticky="new")
        self.element3 = customtkinter.CTkButton(master=self.menu_frame, text="element5", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element3.grid(pady=18, padx=10, row=5, column=0, sticky="new")
        self.change = customtkinter.CTkButton(master=self.menu_frame, text="Change Password", fg_color="transparent",
                                              command=self.change_password, font=("Arial", 26, "normal"))
        
        self.change.grid(pady=18, padx=10, row=6, column=0, sticky="new")
        self.logout = customtkinter.CTkButton(master=self.menu_frame, text="Log out", fg_color="transparent",
                                              command=self.logout, font=("Arial", 26, "normal"))
        
        self.logout.grid(pady=18, padx=10, row=7, column=0, sticky="new")

        self.calendar_frame = customtkinter.CTkFrame(master=self, width=int(screen_width / 3), height=450,
                                                     fg_color='#242424')
        self.calendar_frame.grid(column=0, row=2, sticky="n", rowspan=2)
        self.calendar_frame.grid_columnconfigure(0, weight=1)
        self.calendar_frame.grid_rowconfigure(0, weight=1)
        style = ttk.Style(self)
        style.theme_use('clam') 
        cal = Calendar(self.calendar_frame, selectmode='day', font='Arial 24', background="#242424",
                       disabledbackground="black", bordercolor="black",
                       headersbackground="black", normalbackground="black", foreground='white',
                       normalforeground='white', headersforeground='white', selectbackground='#1f6aa5')
        cal.grid(column=0, row=0, pady=35, padx=15)
        #   -------------------------------- center panel --------------------------------
        self.user_balance_frame = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)), height=400,
                                                         fg_color="green")
        self.user_balance_frame.grid(column=1, row=1, sticky="ns")
        self.user_balance_frame.grid_columnconfigure(0, weight=1)
        self.user_balance_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description2 = customtkinter.CTkLabel(master=self, text="User balance circle graph",
                                                   font=("Arial", 30, "normal"))
        self.description2.grid(pady=18, padx=10, row=1, column=1)

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
                                            text=f"Daily total: {str(round(sum(self.summary.values()), 2))} {self.currency}",
                                            font=("Arial", 30, "normal"))
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

        self.month_view = customtkinter.CTkButton(master=self.spending_summary, text='View details',
                                            command=self.see_month_details, font=('Arial', 30, 'normal'))
        self.month_view.grid(pady=18, padx=10, column=1, row=1)

        self.incoming_transactions_frame = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)),
                                                                  height=160, fg_color="purple")
        self.incoming_transactions_frame.grid(column=1, row=3, sticky="nsw")
        self.incoming_transactions_frame.grid_columnconfigure(0, weight=1)
        self.incoming_transactions_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description4 = customtkinter.CTkLabel(master=self, text="incoming transactions",
                                                   font=("Arial", 30, "normal"))
        self.description4.grid(pady=18, padx=10, column=1, row=3)
        #   -------------------------------- right panel --------------------------------
        self.first_graph_frame = customtkinter.CTkFrame(master=self, width=int(((screen_width / 3) - 20)), height=400)
        self.first_graph_frame.grid(column=2, row=1, sticky="news")
        self.first_graph_frame.grid_columnconfigure(0, weight=1)
        self.first_graph_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        columns = list(self.summary.keys())
        values = list(self.summary.values())

        COLOR = 'white'
        mat.rcParams['text.color'] = COLOR
        mat.rcParams['axes.labelcolor'] = COLOR
        mat.rcParams['xtick.color'] = COLOR
        mat.rcParams['ytick.color'] = COLOR
        
        fig, ax = plt.subplots(figsize=(7, 4.5))
        bars = ax.bar(columns, values)
        ax.bar_label(bars)

        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')

        ax.tick_params(color=COLOR, labelcolor=COLOR)
        for spine in ax.spines.values():
            spine.set_edgecolor(COLOR)

        plt.xlabel('Categories', fontsize=15)
        plt.ylabel(f'Amount [{self.currency}]', fontsize=15)
        plt.title('Day summary', fontsize=20)

        canvas = FigureCanvasTkAgg(fig, self.first_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        plt.close(fig)

        self.second_graph_frame = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)), height=450,
                                                         fg_color="#242424")
        self.second_graph_frame.grid(column=1, columnspan=2, row=2, rowspan=2, sticky="nse")
        self.second_graph_frame.grid_columnconfigure(0, weight=1)
        self.second_graph_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        query = f"SELECT e.amount, c.name, EXTRACT(DAY FROM e.add_date) as day from expenses AS e JOIN " \
                f"users AS u ON e.user_id=u.id JOIN categories AS c ON e.category_id=c.id " \
                f"WHERE u.username='{self.username}' AND EXTRACT(MONTH FROM add_date) = {current_month} " \
                f"AND EXTRACT(YEAR FROM add_date) = {current_year}"

        days_in_month = monthrange(current_year, current_month)[1]

        self.month_results = db.select_data(query)

        self.month_graph_data = {}
        for i in range(1, days_in_month+1):
            self.month_graph_data[i] = {'Entertainment': 0, 'Shopping': 0, 'Bills': 0, 'Subscriptions': 0, 'Other': 0}

        for r in self.month_results:
            for m in self.month_graph_data:
                if int(r[2]) == m:
                    if r[1] == 'Entertainment':
                        self.month_graph_data[m]['Entertainment'] += float(r[0])
                    elif r[1] == 'Shopping':
                        self.month_graph_data[m]['Shopping'] += float(r[0])
                    elif r[1] == 'Bills':
                        self.month_graph_data[m]['Bills'] += float(r[0])
                    elif r[1] == 'Subscriptions':
                        self.month_graph_data[m]['Subscriptions'] += float(r[0])
                    else:
                        self.month_graph_data[m]['Other'] += float(r[0])
        
        x = self.month_graph_data.keys()
        entertainment_list = []
        shopping_list = []
        bills_list = []
        subs_list = []
        other_list = []

        for i in self.month_graph_data:
            for k, v in self.month_graph_data[i].items():
                if k == 'Entertainment':
                    entertainment_list.append(v)
                elif k == 'Shopping':
                    shopping_list.append(v)
                elif k == 'Bills':
                    bills_list.append(v)
                elif k == 'Subscriptions':
                    subs_list.append(v)
                else:
                    other_list.append(v)

        def sum_lists(*lists):
            result = []
            for i in range(len(lists[0])):
                total = 0
                for lst in lists:
                    total += lst[i]
                result.append(total)

            return result
        
        fig, ax = plt.subplots(figsize=(8, 4))

        p1 = ax.bar(x, entertainment_list, width=0.7, bottom=sum_lists(shopping_list, bills_list, subs_list, other_list))
        p2 = ax.bar(x, shopping_list, width=0.7, bottom=sum_lists(bills_list, subs_list, other_list))
        p3 = ax.bar(x, bills_list, width=0.7, bottom=sum_lists(subs_list, other_list))
        p4 = ax.bar(x, subs_list, width=0.7, bottom=other_list)
        p5 = ax.bar(x, other_list, width=0.7)
        ax.set_xticks(range(1, days_in_month+1, 2))
        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')

        canvas = FigureCanvasTkAgg(fig, self.second_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT)

        ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('Entertainment', 'Shopping', 'Bills', 'Subscriptions', 'Other'), loc='best', frameon=False)
        
        plt.close(fig)



    def see_details(self):
        day_summary = DaySummary(self.username, self.summary, self.currency, len(self.results))
        day_summary.mainloop()

    def see_month_details(self):
        month_summary = MonthSummary(self.username, self.month_summary, self.currency, len(self.month_results))
        month_summary.mainloop()

    def get_user_name(self, user_login):
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT name FROM users WHERE username='{user_login}';"
        user_name = db.select_data(name_query, 'one')
        return user_name[0]

    def show_expenses(self):
        self.destroy()
        expenses = AllExpenses(self.username)
        expenses.mainloop()

    def show_revenues(self):
        revenues = AllRevenues(self.username)
        revenues.mainloop()

    def change_password(self):
        changepass = ChangePassword(self.username)
        changepass.mainloop()

    def logout(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, "login_pass.txt")

        if os.path.exists(file_path):
            os.remove(file_path)

        self.destroy()
        login_screen = login.Login()
        login_screen.mainloop()
