from modules.database.database_connect import DatabaseConnector
from datetime import date


class Budget:
    def __init__(self, username):
        self.username = username
        self.db = DatabaseConnector()
        query = f"SELECT balance FROM users WHERE username = '{self.username}'"
        self.balance = self.db.select_data(query, 'one')[0]
        query = f"SELECT id FROM users WHERE username = '{self.username}'"
        self.user_id = self.db.select_data(query, 'one')[0]


    def add_expense(self, name, desc, amount, category):
        '''
        uzycie:
        user = Budget('admin')
        user.add_expense('Testowy wydatek', 'Wydatek wprowadzony dla testow', 2500, 1)
        '''
        if amount > self.balance:
            return 'You do not have enough money!'
        else:
            query = f"INSERT INTO expenses (name, description, amount, add_date, user_id, category_id) VALUES ('{name}', '{desc}', '{amount}', '{date.today()}', '{self.user_id}', '{category}')"
            self.db.make_query(query)
            
            current_balance = self.balance - amount
            query = f"UPDATE users SET balance = {current_balance} WHERE username = '{self.username}'"
            self.db.make_query(query)

    
    def add_revenue(self, name, desc, amount):
        query = f"INSERT INTO revenues (name, description, amount, add_date, user_id) VALUES ('{name}', '{desc}', '{amount}', '{date.today()}', '{self.user_id}')"
        self.db.make_query(query)
        current_balance = self.balance + amount
        query = f"UPDATE users SET balance = {current_balance} WHERE username = '{self.username}'"
        self.db.make_query(query)
