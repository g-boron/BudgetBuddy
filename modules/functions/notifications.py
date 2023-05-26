from modules.database import database_connect
from modules.functions.get_users_info import get_user_id


def get_all_user_notifications(user_id):
    account_id = get_user_id(user_id)
    db = database_connect.DatabaseConnector()
    query = f"SELECT id, invite_from, is_read FROM invites WHERE invite_to = '{account_id}';"
    all_notifications = db.select_data(query)
    return all_notifications


def count_unread_notifications(user_id):
    account_id = get_user_id(user_id)
    db = database_connect.DatabaseConnector()
    query = f"SELECT count(id) FROM invites WHERE is_read = False AND invite_to = {account_id};"
    result = db.select_data(query, 'one')
    return result[0]


def mark_notification_as_read(notification_id):
    db = database_connect.DatabaseConnector()
    query = f"UPDATE invites SET is_read = True WHERE id = {notification_id};"
    db.make_query(query)
