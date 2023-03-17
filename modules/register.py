from tkinter import *
import customtkinter 
import tkinter.messagebox


class Registration:

    customtkinter.set_appearance_mode("light")  
    customtkinter.set_default_color_theme("green")  

    root=customtkinter.CTk()
    root.geometry("700x500")
    root.minsize(700,500)
    root.title="BuddgetBuddy"
    #self.resizable(False, False)

    def register(self):
        tkinter.messagebox.showinfo("Welcome to GFG.",  "Hi I'm your message")
        

    frame=customtkinter.CTkFrame(master=root)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame.grid_rowconfigure(0,weight=1)
    frame.grid_rowconfigure(1,weight=1)
    frame.grid_rowconfigure(2,weight=1)
    frame.grid_rowconfigure(3,weight=1)
    frame.grid_rowconfigure(4,weight=1)
    
    frame.grid_columnconfigure((0,1,2), weight=1)


    label = customtkinter.CTkLabel(master=frame, text="Budget Buddy", font=("Arial", 24 ))
    label.grid(pady=12, padx=10,row=0, column=1)

    login=customtkinter.CTkEntry(master=frame, placeholder_text="Login",height=30)
    login.grid(pady=12, padx=10,row=1, column=1)
    
    password=customtkinter.CTkEntry(master=frame, placeholder_text="Password",show="*",height=30)
    password.grid(pady=12, padx=10, row=2, column=1)

    submit=customtkinter.CTkButton(master=frame, text="Submit",command=Login,height=30)
    submit.grid(pady=12, padx=10, row=3, column=1)

    checkbox=customtkinter.CTkCheckBox(master=frame, text="Remember me")
    checkbox.grid(pady=12, padx=10, row=4, column=1)

    root.mainloop()