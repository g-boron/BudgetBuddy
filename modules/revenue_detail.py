import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
import modules.revenue_edit
from modules.database import database_connect
from modules import all_revenues
from tkinter import messagebox
from modules.revenue_edit import EditRevenue


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class RevenueDetail(customtkinter.CTk):
    def __init__(self, revenue_id, username):
        self.username = username
        self.id = revenue_id
        super().__init__()
        self.geometry("800x600")
        self.title("Revenue detail")
        self.frame = customtkinter.CTkScrollableFrame(master=self, width=700, height=500)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.resizable(False, False)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.window_flag = 1

        db = database_connect.DatabaseConnector()
        query = f"SELECT revenues.id, revenues.name, revenues.description, revenues.add_date, " \
                f"revenues.amount, users.currency, revenues.user_id FROM revenues JOIN users " \
                f"ON revenues.user_id=users.id WHERE revenues.id={self.id}"
        revenue = db.select_data(query, 'one')

        self.name = customtkinter.CTkLabel(master=self.frame, text=revenue[1], font=("Arial", 30, "normal"),
                                           wraplength=200)
        self.name.grid(pady=18, padx=10, row=0, column=0, sticky='nw')

        self.date = customtkinter.CTkLabel(master=self.frame, text=str(revenue[3]).split(' ')[0],
                                           font=("Arial", 30, "normal"))
        self.date.grid(pady=18, padx=10, row=0, column=2, sticky='ne')

        self.desc = customtkinter.CTkLabel(master=self.frame, text=revenue[2], font=("Arial", 30, "normal"),
                                           wraplength=700)
        self.desc.grid(pady=18, padx=10, row=1, column=0, columnspan=3)

        self.amount = customtkinter.CTkLabel(master=self.frame, text=str(revenue[4])+' '+revenue[5],
                                             font=("Arial", 30, "normal"), bg_color='#424543')
        self.amount.grid(pady=18, padx=10, row=2, column=0, sticky='sw')
        id_revenue = revenue[0]

        self.edit = customtkinter.CTkButton(master=self.frame, text='Edit revenue', font=('Arial', 25, 'normal'),
                                            command=lambda id_revenue=id_revenue:
                                            self.edit_revenue(id_revenue, username))
        self.edit.grid(pady=18, padx=10, row=3, column=2)

        self.delete = customtkinter.CTkButton(master=self.frame, text='Delete',
                                              command=lambda id_revenue=id_revenue:
                                              self.delete_revenue(id_revenue, revenue[6], revenue[4]),
                                              font=('Arial', 25, 'normal'))
        self.delete.grid(pady=18, padx=10, row=3, column=0)

    def on_closing(self):
        """Desecrates what will happen after closing the window"""
        self.destroy()
        revenues = all_revenues.AllRevenues(self.username)
        revenues.mainloop()

    def edit_revenue(self, id_revenue, username):
        """Opens revenue edit tab"""
        db = database_connect.DatabaseConnector()
        query = f"SELECT id FROM users WHERE username='{username}'"
        user_id = db.select_data(query, 'one')[0]
        edit_window = modules.revenue_edit.EditRevenue(id_revenue, user_id)
        self.destroy()
        edit_window.mainloop()

    def delete_revenue(self, id_revenue, user_id, amount):
        """Let's user to delete selected revenue"""
        msg_box = messagebox.askquestion('Delete revenue', 'Are you sure you want to delete the revenue?',
                                         icon='warning')
        if msg_box == 'yes':
            db = database_connect.DatabaseConnector()
            query = f"DELETE FROM revenues WHERE id = {id_revenue};"
            db.make_query(query)
            balance = db.select_data(f'SELECT balance FROM users WHERE id={user_id}', 'one')[0]
            db.make_query(f'UPDATE users SET balance = {float(balance) - float(amount)} WHERE id={user_id}')
            self.on_closing()
