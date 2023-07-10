from modules.database import database_connect


def get_user_id(user_id):
    """Returns the id from database of given user"""
    provided_login = user_id
    db = database_connect.DatabaseConnector()
    login_query = f"SELECT id FROM users WHERE username = '{provided_login}';"
    account_id = db.select_data(login_query, 'one')
    if account_id is not None:
        return account_id[0]
    else:
        return False


def get_user_login(user_id):
    """Returns the login from database of given user"""
    db = database_connect.DatabaseConnector()
    login_query = f"SELECT username FROM users WHERE id = {user_id};"
    result = db.select_data(login_query, 'one')
    if result:
        return result
    else:
        return False


def get_user_name(user_login):
    """Returns the name from database of given user"""
    db = database_connect.DatabaseConnector()
    name_query = f"SELECT id, name FROM users WHERE username='{user_login}';"
    user_name = db.select_data(name_query, 'one')
    if user_name:
        return user_name
    else:
        return False