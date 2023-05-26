from modules.database import database_connect
from tkinter import messagebox
from modules.functions.get_users_info import get_user_id


def validate(invited_login):
    """Checks if the given user exists inside the database"""
    provided_login = invited_login
    db = database_connect.DatabaseConnector()
    login_query = f"SELECT id FROM users WHERE username = '{provided_login}';"
    user_id = db.select_data(login_query, 'one')
    if user_id is not None:
        return user_id[0]
    else:
        return False


def send_invitation(inviting_person, invited_login):
    """Sends an invitation from logged account to selected account"""
    invited_person = invited_login
    my_account_id = inviting_person
    db = database_connect.DatabaseConnector()
    query = f"INSERT INTO invites (invite_from, invite_to, is_read) VALUES " \
            f"('{my_account_id}', '{invited_person}', '{0}')"
    db.make_query(query)


def invite_a_friend(inviting_person, invited_login):
    """Validates and then sends an invitation to a selected user"""
    account_login = get_user_id(inviting_person)
    validation = validate(invited_login)
    if validation:
        send_invitation(account_login, validation)
        messagebox.showinfo(title="Success!", message="Invite has been sent!")
    else:
        messagebox.showerror(title="Error", message="Provided login doesn't exist!")

