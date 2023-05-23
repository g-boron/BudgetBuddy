from modules.database import database_connect
from modules.functions.get_user_id import *
from modules.functions.get_user_name import *

def validate_sharing_budget(users_id, owner_id):
    my_id = users_id
    sharing_account = owner_id
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT id FROM shared_budgets WHERE owner_id = {sharing_account} " \
                  f"AND inheriting_id = {my_id};"
    result = db.select_data(check_query, 'one')
    return result


def insert_shared_budget_to_database(users_id, owner_id):
    my_id = users_id
    sharing_account = owner_id
    db = database_connect.DatabaseConnector()
    insert_query = f"INSERT INTO shared_budgets (owner_id, inheriting_id) VALUES ('{sharing_account}', '{my_id}');"
    db.make_query(insert_query)


def check_default_budget(user_id):
    user = int(get_user_id(user_id))
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT inheriting_id FROM shared_budgets WHERE owner_id = {user};"
    check = db.select_data(check_query, 'one')
    user_default = check[0]
    if check is not None:
        return True
    else:
        return False


def check_if_user_is_an_owner(user_id):
    user = int(get_user_id(user_id))
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT owner_id FROM shared_budgets WHERE owner_id = {user};"
    check = db.select_data(check_query, 'one')
    if check is not None:
        return True
    else:
        return False


def get_default_budget(user_id):
    user = int(get_user_id(user_id))
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT inheriting_id FROM shared_budgets WHERE owner_id = {user};"
    check = db.select_data(check_query, 'one')
    user_default = check[0]
    if check is not None:
        return user_default
    else:
        return False

