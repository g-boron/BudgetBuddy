from modules.login import Login
# from modules.database import database_connect


def main():
    login_screen = Login()
    #user_name = login_screen.get_user_name()

    login_screen.mainloop()


if __name__ == '__main__':
    main()
