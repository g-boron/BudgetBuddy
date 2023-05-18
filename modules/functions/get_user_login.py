from modules.database import database_connect


def get_user_login(user_id):
    db = database_connect.DatabaseConnector()
    login_query = f"SELECT username FROM users WHERE id = {user_id};"
    result = db.select_data(login_query, 'one')
    return result
