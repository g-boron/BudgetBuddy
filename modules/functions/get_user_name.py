from modules.database import database_connect


def get_user_name(user_login):
    db = database_connect.DatabaseConnector()
    name_query = f"SELECT id, name FROM users WHERE username='{user_login}';"
    user_name = db.select_data(name_query, 'one')
    return user_name
