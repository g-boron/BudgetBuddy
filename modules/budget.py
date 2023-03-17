from modules.database.database_connect import DatabaseConnector


class Budget:
    def __init__(self, username):
        db = DatabaseConnector()
        query = f"SELECT balance FROM users WHERE username = '{username}'"
        self.balance = db.select_data(query, 'one')

    
    def get_balance(self):
        return self.balance
