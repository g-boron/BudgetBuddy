from tkinter import *
import customtkinter 


class Registration():

    customtkinter.set_appearance_mode("System")  
    customtkinter.set_default_color_theme("green")  

    root=customtkinter.CTk()
    root.geometry("500x350")
    root.minsize(500,350)
    root.title="BuddgetBuddy"
    #self.resizable(False, False)

    def Login():
        print("Test")

    frame=customtkinter.CTkFrame(master=root,width=1000, height=350)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame.grid_rowconfigure(0,weight=1)
    frame.grid_rowconfigure(1,weight=1)
    frame.grid_rowconfigure(2,weight=1)
    frame.grid_rowconfigure(3,weight=1)
    frame.grid_rowconfigure(4,weight=1)
    
    frame.grid_columnconfigure((0,1,2), weight=1)


    label = customtkinter.CTkLabel(master=frame, text="Budget Buddy", font=("Arial", 24 ))
    label.grid(pady=12, padx=10,row=0, column=1)

    entery1=customtkinter.CTkEntry(master=frame, placeholder_text="Login")
    entery1.grid(pady=12, padx=10,row=1, column=1)
    
    entery2=customtkinter.CTkEntry(master=frame, placeholder_text="Password",show="*")
    entery2.grid(pady=12, padx=10, row=2, column=1)

    button=customtkinter.CTkButton(master=frame, text="Login",command=Login)
    button.grid(pady=12, padx=10, row=3, column=1)

    checkbox=customtkinter.CTkCheckBox(master=frame, text="Remember me")
    checkbox.grid(pady=12, padx=10, row=4, column=1)

    root.mainloop()