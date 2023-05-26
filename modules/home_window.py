import datetime
from tkinter import *
import textwrap
from tkinter import ttk
import customtkinter
from PIL import ImageTk
import modules.database.database_connect
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
from modules.app_settings import ApplicationSettings
from modules.functions.notifications import *
from modules.notifications import Notifications
from modules.budget_prediction import BudgetPrediction
from modules.choose_budget import ChooseBudget
from modules.functions.sharing_budgets import *
from modules.payment_term import PaymentTerm
from modules.add_spend_limit import SpendLimit
from .functions.summaries import get_user_currency, get_daily_summary, get_month_summary, generate_month_graph_data, \
    sum_lists, get_spend_limit
from modules.functions.change_theme import set_theme
from modules.functions.send_email import *
from modules.functions.get_users_info import *


class HomeWindow(customtkinter.CTk):
    def __init__(self, user_login):
        self.username = user_login
        set_theme(user_login)
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
        file_flag = self.check_flag()

        #   -------------------------------- top panel --------------------------------
        self.logo = PhotoImage(file="./images/logo_transparent_small.png")
        self.canvas = Canvas(width=140, height=150, bg="#242424", highlightthickness=0)
        self.canvas.create_image(90, 101, image=self.logo)
        self.canvas.grid(column=0, row=0, padx=0, pady=0, sticky="nw")
        self.label = customtkinter.CTkLabel(master=self, text=f"Welcome {get_user_name(self.username)[1]}, "
                                                              f"your budget: {self.get_user_balance(self.username)} "
                                                              f"{self.get_user_currency(self.username)}",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=30, padx=10, row=0, column=1, sticky="nw")
        #   -------------------------------- left panel --------------------------------
        self.menu_frame = customtkinter.CTkScrollableFrame(master=self, width=int(((screen_width / 3) - 20)),
                                                           height=440)
        self.menu_frame.grid(column=0, row=1, sticky="n")
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8 ,9 ,10), weight=1)
        self.label = customtkinter.CTkLabel(master=self.menu_frame, text="Main menu",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=18, padx=10, row=0, column=0)

        self.expenses = customtkinter.CTkButton(master=self.menu_frame, text="My expenses", fg_color="transparent",
                                                font=("Arial", 26, "normal"), command=self.show_expenses)
        self.expenses.grid(pady=18, padx=10, row=1, column=0, sticky="new")

        self.revenues = customtkinter.CTkButton(master=self.menu_frame, text="My revenues", fg_color="transparent",
                                                font=("Arial", 26, "normal"), command=self.show_revenues)
        self.revenues.grid(pady=18, padx=10, row=2, column=0, sticky="new")

        self.payment_term = customtkinter.CTkButton(master=self.menu_frame, text="Payment term", fg_color="transparent",
                                                    font=("Arial", 26, "normal"),
                                                    command=lambda: self.show_payment_payments())
        self.payment_term.grid(pady=18, padx=10, row=3, column=0, sticky="new")

        self.notifications = customtkinter.CTkButton(master=self.menu_frame, text="Notifications",
                                                     fg_color="transparent", font=("Arial", 26, "normal"),
                                                     command=lambda: self.open_notifications(self.username))
        self.notifications.grid(pady=18, padx=10, row=4, column=0, sticky="new")
        self.display_number_of_notifications()
        self.prediction = customtkinter.CTkButton(master=self.menu_frame, text="Budget prediction",
                                                  fg_color="transparent", font=("Arial", 26, "normal"),
                                                  command=self.show_prediction)
        self.prediction.grid(pady=18, padx=10, row=5, column=0, sticky="new")

        self.choose_budget = customtkinter.CTkButton(master=self.menu_frame, text="Budget button",
                                                     fg_color="transparent", font=("Arial", 26, "normal"),
                                                     command=lambda: self.select_budget(self.username))
        self.choose_budget.grid(pady=18, padx=10, row=6, column=0, sticky="new")
        if file_flag:
            self.show_default_budget()
        else:
            self.show_choose_budget()

        self.add_limit = customtkinter.CTkButton(master=self.menu_frame, text="Add monthly expanses limit",
                                                 fg_color="transparent", font=("Arial", 26, "normal"),
                                                 command=lambda: self.spend_limit(self.username))
        self.add_limit.grid(pady=18, padx=10, row=8, column=0, sticky="new")

        self.app_settings_button = customtkinter.CTkButton(master=self.menu_frame, text="App Settings",
                                                           fg_color="transparent", font=("Arial", 26, "normal"),
                                                           command=lambda: self.app_settings(self.username))
        self.app_settings_button.grid(pady=18, padx=10, row=9, column=0, sticky="new")
        self.change = customtkinter.CTkButton(master=self.menu_frame, text="Change Password", fg_color="transparent",
                                              command=self.change_password, font=("Arial", 26, "normal"))
        
        self.change.grid(pady=18, padx=10, row=10, column=0, sticky="new")
        self.logout = customtkinter.CTkButton(master=self.menu_frame, text="Log out", fg_color="transparent",
                                              command=self.logout, font=("Arial", 26, "normal"))
        self.logout.grid(pady=18, padx=10, row=11, column=0, sticky="new")

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
                                                         fg_color="#242424")
        self.user_balance_frame.grid(column=1, row=1, sticky="ns")
        self.user_balance_frame.grid_columnconfigure(0, weight=1)
        self.user_balance_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        
        self.currency = get_user_currency(self.username)
        self.month_summary, self.month_results = get_month_summary(self.username)

        COLOR = 'white'
        mat.rcParams['text.color'] = COLOR
        mat.rcParams['axes.labelcolor'] = COLOR
        mat.rcParams['xtick.color'] = COLOR
        mat.rcParams['ytick.color'] = COLOR

        try:
            limit = float(get_spend_limit(self.username))
        except TypeError:
            limit = None

        if limit is not None:    
            total_expenses = round(sum(self.month_summary.values()), 2)
            limit_left = limit - total_expenses

            values = [total_expenses, limit_left]
            labels = ['Total expenses', 'Limit left']
            fig, ax = plt.subplots(figsize=(5, 4.25))
            fig.patch.set_facecolor('#242424')
            ax.set_facecolor('#242424')
            ax.pie(values, labels=labels, autopct='%1.1f%%', explode=(0, 0.1), textprops={'fontsize': 12})
            plt.title('Remaining spend limit', fontsize=18)
            canvas = FigureCanvasTkAgg(fig, self.user_balance_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
            plt.close(fig)
        else:
            self.error = customtkinter.CTkLabel(master=self.user_balance_frame, text="Set your spending limit to see "
                                                                                     "a pie chart.",
                                                font=("Arial", 25, "normal"))
            self.error.grid(pady=18, padx=10, column=0, row=3)

        self.summary, self.results = get_daily_summary(self.username)

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

        self.month_total = customtkinter.CTkLabel(master=self.spending_summary,
                                                  text=f"Month total: {str(round(sum(self.month_summary.values()), 2))}"
                                                       f" {self.currency}", font=("Arial", 30, "normal"))
        self.month_total.grid(pady=18, padx=10, column=0, row=1)

        self.month_view = customtkinter.CTkButton(master=self.spending_summary, text='View details',
                                                  command=self.see_month_details, font=('Arial', 30, 'normal'))
        self.month_view.grid(pady=18, padx=10, column=1, row=1)

        self.incoming_transactions_frame = customtkinter.CTkScrollableFrame(master=self,
                                                                            width=int((screen_width / 3)), height=160)
        self.incoming_transactions_frame.grid(column=1, row=3, sticky="nsw")
        self.incoming_transactions_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.incoming_transactions_frame.grid_rowconfigure((0,1, 2 ), weight=1)
        
        self.show_incoming_payments(self.username)
        #   -------------------------------- right panel --------------------------------
        self.first_graph_frame = customtkinter.CTkFrame(master=self, width=int(((screen_width / 3) - 20)), height=400,)
        self.first_graph_frame.grid(column=2, row=1, sticky="news")
        self.first_graph_frame.grid_columnconfigure(0, weight=1)
        self.first_graph_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        columns = list(self.summary.keys())
        values = list(self.summary.values())

        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        bars = ax.bar(columns, values)

        for c in ax.containers:
            labels = [v if v > 0 else "" for v in c.datavalues]    
            ax.bar_label(c, labels=labels)

        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')

        ax.tick_params(color=COLOR, labelcolor=COLOR)
        for spine in ax.spines.values():
            spine.set_edgecolor(COLOR)

        plt.xlabel('Categories', fontsize=11)
        plt.ylabel(f'Amount [{self.currency}]', fontsize=11)
        plt.title('Day summary', fontsize=18)

        canvas = FigureCanvasTkAgg(fig, self.first_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        plt.close(fig)

        self.second_graph_frame = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)), height=450,
                                                         fg_color="#242424")
        self.second_graph_frame.grid(column=1, columnspan=2, row=2, rowspan=2, sticky="nse")
        self.second_graph_frame.grid_columnconfigure(0, weight=1)
        self.second_graph_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        x, days_in_month, entertainment_list, shopping_list, bills_list, subs_list, \
            other_list = generate_month_graph_data(self.username)
        
        fig, ax = plt.subplots(figsize=(7.5, 4))

        p1 = ax.bar(x, entertainment_list, bottom=sum_lists(shopping_list, bills_list, subs_list, other_list))
        p2 = ax.bar(x, shopping_list, bottom=sum_lists(bills_list, subs_list, other_list))
        p3 = ax.bar(x, bills_list, bottom=sum_lists(subs_list, other_list))
        p4 = ax.bar(x, subs_list, bottom=other_list)
        p5 = ax.bar(x, other_list)
        ax.set_xticks(range(1, days_in_month+1, 2))
        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')

        plt.xlabel('Days in month', fontsize=11)
        plt.ylabel(f'Amount [{self.currency}]', fontsize=11)
        plt.title('Month summary', fontsize=18)

        for spine in ax.spines.values():
            spine.set_edgecolor(COLOR)

        canvas = FigureCanvasTkAgg(fig, self.second_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT)

        ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('Entertainment', 'Shopping', 'Bills', 'Subscriptions', 'Other'),
                  loc='best', frameon=False)
        
        plt.close(fig)

    def see_details(self):
        day_summary = DaySummary(self.username, len(self.results))
        day_summary.mainloop()

    def see_month_details(self):
        month_summary = MonthSummary(self.username, len(self.month_results))
        month_summary.mainloop()

    def show_expenses(self):
        self.destroy()
        expenses = AllExpenses(self.username)
        expenses.mainloop()

    def show_revenues(self):
        self.destroy()
        revenues = AllRevenues(self.username)
        revenues.mainloop()

    def change_password(self):
        change_password = ChangePassword(self.username)
        change_password.mainloop()

    def logout(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, "login_pass.txt")

        if os.path.exists(file_path):
            os.remove(file_path)

        self.destroy()
        login_screen = login.Login()
        login_screen.mainloop()

    def app_settings(self, username):
        self.destroy()
        setting_window = ApplicationSettings(username)
        setting_window.mainloop()

    def open_notifications(self, username):
        self.destroy()
        notification_tab = Notifications(username)
        notification_tab.mainloop()

    def show_prediction(self):
        db = database_connect.DatabaseConnector()
        user_id = db.select_data(f"SELECT id FROM users WHERE username='{self.username}'", 'one')[0]
        prediction = BudgetPrediction(user_id, self.currency)
        prediction.mainloop()

    def show_payment_payments(self):
        self.destroy()
        payment_payments_tab = PaymentTerm(self.username)
        payment_payments_tab.mainloop()

    def display_number_of_notifications(self):
        number_of_unread_notifications = count_unread_notifications(self.username)
        if number_of_unread_notifications > 0:
            self.notifications.configure(text=f"Notifications [{number_of_unread_notifications}]", text_color="red")
            db = database_connect.DatabaseConnector()
            query = f"SELECT email FROM users WHERE username = '{self.username}'"
            email = db.select_data(query, 'one')
            send_notification_email(self.username, email)

    def show_choose_budget(self):
        self.choose_budget.configure(text="Change budget")

    def show_default_budget(self):
        self.choose_budget.configure(text="Default budget")

    def check_if_there_are_shared_budgets(self):
        user_id = get_user_id(self.username)
        db = database_connect.DatabaseConnector()
        check_query = f"SELECT id FROM shared_budgets WHERE inherited_id = {user_id};"
        result = db.select_data(check_query, 'one')
        if result is None:
            self.choose_budget.grid_forget()

    def select_budget(self, username):
        self.destroy()
        budget_selector = ChooseBudget(username)
        budget_selector.mainloop()

    def get_user_balance(self, user_login):
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT balance FROM users WHERE username='{user_login}';"
        user_name = db.select_data(name_query, 'one')
        return str(user_name[0])
    
    def get_user_currency(self, user_login):
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT currency FROM users WHERE username='{user_login}';"
        user_name = db.select_data(name_query, 'one')
        return str(user_name[0])
    
    def spend_limit(self, username):
        self.destroy()
        setting_window = SpendLimit(username)
        setting_window.mainloop()
        
    def show_incoming_payments(self, username):
        db = database_connect.DatabaseConnector()
        query = f"SELECT name, date, amount, id FROM payment_term " \
                f"WHERE user_id={get_user_id(username)} "
                
        payments = db.select_data(query)

        for idx, payments in enumerate(payments):
            payment_term_name = customtkinter.CTkLabel(master=self.incoming_transactions_frame,
                                                       text=textwrap.shorten(payments[0], width=25, placeholder='...'),
                                                       font=("Arial", 18, "normal"))
            payment_term_name.grid(pady=20, padx=10, row=idx, column=0)

            date = customtkinter.CTkLabel(master=self.incoming_transactions_frame, text=str(payments[1]).split(' ')[0],
                                          font=("Arial", 18, "normal"))
            date.grid(pady=20, padx=10, row=idx, column=1)

            amount = customtkinter.CTkLabel(master=self.incoming_transactions_frame, text=payments[2],
                                            font=("Arial", 18, "normal"))
            amount.grid(pady=20, padx=10, row=idx, column=2)

    def check_flag(self):
        with open('budget_flag.txt', 'r') as file:
            content = file.read()
        return content
