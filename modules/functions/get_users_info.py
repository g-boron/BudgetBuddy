from modules.database import database_connect


def get_user_id(user_id):
    provided_login = user_id
    db = database_connect.DatabaseConnector()
    login_query = f"SELECT id FROM users WHERE username = '{provided_login}';"
    account_id = db.select_data(login_query, 'one')
    if account_id is not None:
        return account_id[0]
    else:
        return False


def get_user_login(user_id):
    db = database_connect.DatabaseConnector()
    login_query = f"SELECT username FROM users WHERE id = {user_id};"
    result = db.select_data(login_query, 'one')
    return result


def get_user_name(user_login):
    db = database_connect.DatabaseConnector()
    name_query = f"SELECT id, name FROM users WHERE username='{user_login}';"
    user_name = db.select_data(name_query, 'one')
    return user_name
