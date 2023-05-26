import customtkinter
from modules.database.database_connect import DatabaseConnector
from modules.functions.get_users_info import *


def set_theme(user_id):
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
       