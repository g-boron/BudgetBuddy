from modules.login import Login
import tkinter
import customtkinter
from modules.database import database_connect


def main():
    login_screen = Login()

    login_screen.mainloop()


if __name__ == '__main__':
    main()
