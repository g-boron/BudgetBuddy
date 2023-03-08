
from tkinter import *
import customtkinter 


customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  



app = customtkinter.CTk()  # create CTk window 
app.title("Budget Buddy")
app.geometry("800x500")
app.minsize(800, 500)



# tworzenie etykiety "Email"
email_label = customtkinter.CTkLabel(master=app, text="E-mail",font=("Arial", 22))
email_label.pack(side=TOP, expand=YES)

# tworzenie pola do wprowadzania emaila
email_entry = customtkinter.CTkEntry(master=app, placeholder_text="CTkEntry",corner_radius=8)
email_entry.pack(side=TOP, expand=YES)

# tworzenie etykiety "Hasło"
password_label = customtkinter.CTkLabel(master=app, text="Hasło",font=("Arial", 22))
password_label.pack(side=TOP, expand=YES)

# tworzenie pola do wprowadzania hasła
password_entry = customtkinter.CTkEntry(master=app, placeholder_text="CTkEntry",show="*",corner_radius=8)
password_entry.pack(side=TOP, expand=YES)




app.mainloop() #listening to events