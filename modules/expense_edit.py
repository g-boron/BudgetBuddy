import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.budget import Budget
from tkcalendar import Calendar
from tkinter import ttk


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class EditExpense(customtkinter.CTk):
    def __init__(self, expense_id):
        self.id_exp = expense_id
        super().__init__()
        self.geometry("800x800")
        self.title("Edit your expense")
        self.frame = customtkinter.CTkFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.window_flag = 1

        self.label = customtkinter.CTkLabel(master=self.frame, text="Edit this expense", font=("Arial", 35, "normal"))
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
