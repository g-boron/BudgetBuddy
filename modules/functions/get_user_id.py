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
