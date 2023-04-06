import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class RevenueDetail(customtkinter.CTk):
    def __init__(self, revenue_id):
        self.id = revenue_id
        super().__init__()
        self.geometry("800x600")
        self.title("Revenue detail")
        self.frame = customtkinter.CTkScrollableFrame(master=self, width=700, height=500)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.window_flag = 1

        db = database_connect.DatabaseConnector()
        query = f"SELECT revenues.name, revenues.description, revenues.add_date, revenues.amount, revenues.id, users.currency FROM revenues JOIN users ON revenues.user_id=users.id WHERE revenues.id={self.id}"
        revenue = db.select_data(query, 'one')

        self.name = customtkinter.CTkLabel(master=self.frame, text=revenue[0], font=("Arial", 30, "normal"),
                                           wraplength=200)
        self.name.grid(pady=18, padx=10, row=0, column=0, sticky='nw')

        self.date = customtkinter.CTkLabel(master=self.frame, text=revenue[2], font=("Arial", 30, "normal"))
        self.date.grid(pady=18, padx=10, row=0, column=2, sticky='ne')

        self.desc = customtkinter.CTkLabel(master=self.frame, text=revenue[1], font=("Arial", 30, "normal"),
                                           wraplength=700)
        self.desc.grid(pady=18, padx=10, row=1, column=0, columnspan=3)

        self.amount = customtkinter.CTkLabel(master=self.frame, text=str(revenue[3]) + ' ' + revenue[5],
                                             font=("Arial", 30, "normal"), bg_color='#424543')
        self.amount.grid(pady=18, padx=10, row=2, column=0, sticky='sw')
