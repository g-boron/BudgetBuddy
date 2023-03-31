import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect


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
                                                           height=400)
        self.menu_frame.grid(column=0, row=1, sticky="n")
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.label = customtkinter.CTkLabel(master=self.menu_frame, text="Main menu",
                                            font=("Arial", 30, "normal"))
        self.label.grid(pady=18, padx=10, row=0, column=0)
        self.element1 = customtkinter.CTkButton(master=self.menu_frame, text="element1", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element1.grid(pady=18, padx=10, row=1, column=0, sticky="new")
        self.element2 = customtkinter.CTkButton(master=self.menu_frame, text="element2", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element2.grid(pady=18, padx=10, row=2, column=0, sticky="new")
        self.element3 = customtkinter.CTkButton(master=self.menu_frame, text="element3", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element3.grid(pady=18, padx=10, row=3, column=0, sticky="new")
        self.element3 = customtkinter.CTkButton(master=self.menu_frame, text="element4", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element3.grid(pady=18, padx=10, row=4, column=0, sticky="new")
        self.element3 = customtkinter.CTkButton(master=self.menu_frame, text="element5", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element3.grid(pady=18, padx=10, row=5, column=0, sticky="new")
        self.element3 = customtkinter.CTkButton(master=self.menu_frame, text="element6", fg_color="transparent",
                                                font=("Arial", 26, "normal"))
        self.element3.grid(pady=18, padx=10, row=6, column=0, sticky="new")

        self.calendar_frame = customtkinter.CTkFrame(master=self, width=(screen_width / 3), height=450, fg_color="blue")
        self.calendar_frame.grid(column=0, row=2, sticky="n", rowspan=2)
        self.calendar_frame.grid_columnconfigure(0, weight=1)
        self.calendar_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description1 = customtkinter.CTkLabel(master=self, text="Calendar", font=("Arial", 30, "normal"))
        self.description1.grid(pady=18, padx=10, row=2, column=0)
        #   -------------------------------- center panel --------------------------------
        self.user_balance_frame = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)), height=400,
                                                         fg_color="green")
        self.user_balance_frame.grid(column=1, row=1, sticky="ns")
        self.user_balance_frame.grid_columnconfigure(0, weight=1)
        self.user_balance_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description2 = customtkinter.CTkLabel(master=self, text="User balance circle graph",
                                                   font=("Arial", 30, "normal"))
        self.description2.grid(pady=18, padx=10, row=1, column=1)

        self.today_spending_frame = customtkinter.CTkScrollableFrame(master=self, width=int(((screen_width / 3) - 20)),
                                                                     height=270, fg_color="white")
        self.today_spending_frame.grid(column=1, row=2, sticky="ns")
        self.today_spending_frame.grid_columnconfigure(0, weight=1)
        self.today_spending_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description3 = customtkinter.CTkLabel(master=self, text="User's today spending",
                                                   font=("Arial", 30, "normal"))
        self.description3.grid(pady=18, padx=10, column=1, row=2)

        self.incoming_transactions_frame = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)),
                                                                  height=160, fg_color="purple")
        self.incoming_transactions_frame.grid(column=1, row=3, sticky="ns")
        self.incoming_transactions_frame.grid_columnconfigure(0, weight=1)
        self.incoming_transactions_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description4 = customtkinter.CTkLabel(master=self, text="incoming transactions",
                                                   font=("Arial", 30, "normal"))
        self.description4.grid(pady=18, padx=10, column=1, row=3)
        #   -------------------------------- right panel --------------------------------
        self.first_graph_frame = customtkinter.CTkFrame(master=self, width=int(((screen_width / 3) - 20)), height=400,
                                                        fg_color="red")
        self.first_graph_frame.grid(column=2, row=1, sticky="news")
        self.first_graph_frame.grid_columnconfigure(0, weight=1)
        self.first_graph_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description5 = customtkinter.CTkLabel(master=self, text="first graph",
                                                   font=("Arial", 30, "normal"))
        self.description5.grid(pady=18, padx=10, column=2, row=1)

        self.second_graph_frame = customtkinter.CTkFrame(master=self, width=int((screen_width / 3)), height=450,
                                                         fg_color="orange")
        self.second_graph_frame.grid(column=2, row=2, rowspan=2, sticky="new")
        self.second_graph_frame.grid_columnconfigure(0, weight=1)
        self.second_graph_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.description6 = customtkinter.CTkLabel(master=self, text="second graph", font=("Arial", 30, "normal"))
        self.description6.grid(pady=18, padx=10, row=2, column=2)

    def get_user_name(self, user_login):
        db = database_connect.DatabaseConnector()
        name_query = f"SELECT name FROM users WHERE username='{user_login}';"
        user_name = db.select_data(name_query, 'one')
        return user_name[0]
