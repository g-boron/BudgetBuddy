from tkinter import *
import customtkinter
from PIL import ImageTk
from modules.database import database_connect
from tkinter import messagebox
from modules.functions.invite_to_budget import *
import modules.database.database_connect
from modules.database import database_connect
from modules.functions.get_user_name import *
from modules.functions.get_user_id import *



def set_theme(self,user_id):

    user = int(get_user_id(user_id))

    db = database_connect.DatabaseConnector()

    query = f"SELECT theme FROM users " \
            f"WHERE id={user} "
    
    theme = db.select_data(query, 'one')

    if theme[0] == "light":
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue")
       

    elif theme[0] == "dark":
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

    return theme[0]
       