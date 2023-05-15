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


def get_all_user_notifications(user_id):
    account_id = get_user_id(user_id)
    db = database_connect.DatabaseConnector()
    query = f"SELECT id, invite_from FROM invites WHERE invite_to = '{account_id}';"
    all_notifications = db.select_data(query)
    return all_notifications


