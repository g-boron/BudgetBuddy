from modules.login import Login
from modules.register import Register
# from modules.database import database_connect


def main():
    
    register_screen = Register()

    register_screen.mainloop()
    
    
    #login_screen = Login()

    #login_screen.mainloop()


if __name__ == '__main__':
    main()
