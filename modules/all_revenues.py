import tkinter
from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from modules.revenue_detail import RevenueDetail
from modules.add_revenue import AddRevenue
from modules import home_window
import textwrap
from modules.functions.get_users_info import get_user_name

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class AllRevenues(customtkinter.CTk):
    def __init__(self, user_login):
        self.username = user_login
        super().__init__()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.state('zoomed')
        self.title("See all your revenues")
        self.wm_iconbitmap()
        self.iconpath = ImageTk.PhotoImage(file="./images/logo_transparent.png")
        self.iconphoto(False, self.iconpath)
        self.resizable(True, True)
        self.label = customtkinter.CTkLabel(master=self, text=f"{get_user_name(self.username)[1]}'s revenues",
                                            font=("Arial", 50, "normal"))
        self.label.pack(pady=50)

        self.frame = customtkinter.CTkScrollableFrame(master=self, width=800, height=600)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

# input field to type name of revenue
        self.name_entry = customtkinter.CTkEntry(master=self, placeholder_text="name", justify=CENTER,
                                                 font=('Arial', 30, 'normal'), width=200)
        self.name_entry.place(x=700, y=150)

# choose filter option
        self.filter_option = customtkinter.CTkOptionMenu(self, values=['Date descending', 'Date ascending',
                                                                       'Amount descending', 'Amount ascending'],
                                                         font=('Arial', 30, 'normal'))
        self.filter_option.place(x=1150, y=150)

        self.refresh()

        self.add_button = customtkinter.CTkButton(master=self, text='Add new revenue', command=self.add_new_expense,
                                                  font=('Arial', 30, 'normal'))
        self.add_button.place(relx=0.2, rely=0.9, anchor='center')

        self.refresh_button = customtkinter.CTkButton(master=self, text='Refresh', command=self.refresh,
                                                      font=('Arial', 30, 'normal'))
        self.refresh_button.place(relx=0.5, rely=0.9, anchor='center')

        self.exit_button = customtkinter.CTkButton(master=self, text='Exit', command=lambda: self.on_closing(),
                                                   font=('Arial', 30, 'normal'))
        self.exit_button.place(relx=0.8, rely=0.9, anchor='center')

    def on_closing(self):
        self.destroy()
        home = home_window.HomeWindow(self.username)
        home.mainloop()

    def see_details(self, rev_id):
        self.destroy()
        rev_detail = RevenueDetail(rev_id, self.username)
        rev_detail.mainloop()

    def add_new_expense(self):
        self.destroy()
        add_rev = AddRevenue(get_user_name(self.username)[0])
        add_rev.mainloop()
    
    def refresh(self):
        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        db = database_connect.DatabaseConnector()

        name = self.name_entry.get()
        choosed_filter = self.filter_option.get()

        if filter == 'Amount descending':
            sort_filter = 'amount DESC'
        elif filter == 'Amount ascending':
            sort_filter = 'amount ASC'
        elif filter == 'Date descending':
            sort_filter = 'add_date DESC'
        else:
            sort_filter = 'add_date ASC'

        query = f"SELECT name, description, add_date, amount, id FROM revenues " \
                f"WHERE user_id={get_user_name(self.username)[0]} "\
                f"AND name LIKE '%{name}%' ORDER BY {sort_filter}"

        revenues = db.select_data(query)
        for idx, revenue in enumerate(revenues):
            revenue_name = customtkinter.CTkLabel(master=self.frame,
                                                  text=textwrap.shorten(revenue[0], width=25,
                                                                        placeholder='...'),
                                                  font=("Arial", 24, "normal"))
            revenue_name.grid(pady=20, padx=10, row=idx, column=0)
            
            date = customtkinter.CTkLabel(master=self.frame, text=str(revenue[2]).split(' ')[0],
                                          font=("Arial", 24, "normal"))
            date.grid(pady=20, padx=10, row=idx, column=1)

            price = customtkinter.CTkLabel(master=self.frame, text=revenue[3], font=("Arial", 24, "normal"))
            price.grid(pady=20, padx=10, row=idx, column=2)
            
            revenue_id = revenue[4]

            detail_button = customtkinter.CTkButton(master=self.frame, text="Detail",
                                                    command=lambda rev_id=revenue_id: self.see_details(rev_id),
                                                    font=('Arial', 24, 'normal'))
            detail_button.grid(pady=20, padx=10, row=idx, column=3)
