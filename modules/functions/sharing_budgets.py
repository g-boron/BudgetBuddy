from modules.database import database_connect


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
