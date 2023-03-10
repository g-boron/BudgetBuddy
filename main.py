from modules.login import Login


#from modules.database import database_connect


def main():
    login_screen = Login()
    login_screen.wm_iconbitmap("/images/budget_buddy_icon.ico")
    login_screen.mainloop()


if __name__ == '__main__':
    main()
