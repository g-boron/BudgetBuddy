from tkinter import *
import customtkinter
from PIL import ImageTk

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class HomeWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        width = self.winfo_screenwidth()
        height = self.winfo_height()
        #self.geometry("%dx%d" % (width, height))
        self.title("Main window")
        self.frame = customtkinter.CTkFrame(master=self, width=width, height=height)
        self.wm_iconbitmap()
        #self.iconpath = ImageTk.PhotoImage(file="./images/logo_dark.png")
        #self.iconphoto(False, self.iconpath)
        self.label = customtkinter.CTkLabel(master=self.frame, text="Welcome to home screen",
                                            font=("Arial", 30, "normal"))

        self.resizable(False, False)
        self.label.pack()