from modules.database import database_connect
from modules.functions.get_users_info import *
from modules.functions.get_users_info import get_user_id


def validate_sharing_budget(users_id, owner_id):
    """Checks if given user is sharing budget with currently logged account"""
    my_id = users_id
    sharing_account = owner_id
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT id FROM shared_budgets WHERE owner_id = {sharing_account} " \
                  f"AND inheriting_id = {my_id};"
    result = db.select_data(check_query, 'one')
    return result


def insert_shared_budget_to_database(users_id, owner_id):
    """Inserts owner and inheriting ids to database"""
    my_id = users_id
    sharing_account = owner_id
    db = database_connect.DatabaseConnector()
    insert_query = f"INSERT INTO shared_budgets (owner_id, inheriting_id) VALUES ('{sharing_account}', '{my_id}');"
    db.make_query(insert_query)


def check_default_budget(user_id):
    """Checks if currently logged user has it's own budget"""
    user = int(get_user_id(user_id))
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT inheriting_id FROM shared_budgets WHERE owner_id = {user};"
    check = db.select_data(check_query, 'one')
    if check is not None:
        return True
    else:
        return False


def check_if_user_is_an_owner(user_id):
    """Checks if currently logged user is sharing it's budget with someone"""
    user = int(get_user_id(user_id))
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT owner_id FROM shared_budgets WHERE owner_id = {user};"
    check = db.select_data(check_query, 'one')
    if check is not None:
        with open('budget_flag.txt', 'w') as file:
            file.write('a')
        return True
    else:
        with open('budget_flag.txt', 'w') as file:
            file.write('')
        return False


def get_default_budget(user_id):
    """Gets the information about logged user's default budget"""
    user = int(get_user_id(user_id))
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT inheriting_id FROM shared_budgets WHERE owner_id = {user};"
    check = db.select_data(check_query, 'one')
    user_default = check[0]
    if check is not None:
        return user_default
    else:
        return False


def check_which_button_to_display(user_id):
    """Checks which button to display on home screen of the application"""
    logged_user = int(get_user_id(user_id))
    db = database_connect.DatabaseConnector()
    check_query = f"SELECT id FROM shared_budgets WHERE owner_id = {logged_user};"
    result = db.select_data(check_query)
    if result:
        return True
    else:
        return False

