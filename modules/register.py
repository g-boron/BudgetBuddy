
from tkinter import *
import customtkinter 


customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  



app = customtkinter.CTk()  # create CTk window 
app.title("Budget Buddy")
app.geometry("800x500")
app.minsize(800, 500)

app.columnconfigure(0,weight=2)
app.columnconfigure(1,weight=1)

app.rowconfigure(0,weight=1)
app.rowconfigure(1,weight=1)
app.rowconfigure(2,weight=1)
app.rowconfigure(3,weight=1)
app.rowconfigure(4,weight=1)



# tworzenie etykiety "Email"
email_label = customtkinter.CTkLabel(master=app, text="E-mail",font=("Arial", 22))
email_label.grid(column=0,row=0)

# tworzenie pola do wprowadzania emaila
email_entry = customtkinter.CTkEntry(master=app, placeholder_text="CTkEntry",corner_radius=8)
email_entry.grid(column=0,row=1)

# tworzenie etykiety "Hasło"
password_label = customtkinter.CTkLabel(master=app, text="Hasło",font=("Arial", 22))
password_label.grid(column=0,row=3)

# tworzenie pola do wprowadzania hasła
password_entry = customtkinter.CTkEntry(master=app, placeholder_text="CTkEntry",show="*",corner_radius=8)
password_entry.grid(column=0,row=4)




app.mainloop() #listening to events