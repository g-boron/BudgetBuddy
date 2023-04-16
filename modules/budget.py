from modules.database.database_connect import DatabaseConnector
from datetime import datetime


class Budget:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = DatabaseConnector()
        query = f"SELECT balance FROM users WHERE id = '{self.user_id}'"
        self.balance = float(self.db.select_data(query, 'one')[0])


    def add_expense(self, name, desc, amount, category, day):
        '''
        uzycie:
        user = Budget('admin')
        user.add_expense('Testowy wydatek', 'Wydatek wprowadzony dla testow', 2500, 1)
        '''
        if amount > self.balance:
            return False
        else:
            query = f"INSERT INTO expenses (name, description, amount, add_date, user_id, category_id) VALUES ('{name}', '{desc}', '{amount}', '{day}', '{self.user_id}', '{category}')"
            self.db.make_query(query)
            
            current_balance = self.balance - amount
            query = f"UPDATE users SET balance = {current_balance} WHERE id = '{self.user_id}'"
            self.db.make_query(query)
            return True

    
    def add_revenue(self, name, desc, amount, day):
        query = f"INSERT INTO revenues (name, description, amount, add_date, user_id) VALUES ('{name}', '{desc}', '{amount}', '{day}', '{self.user_id}')"
        self.db.make_query(query)
        current_balance = self.balance + amount
        query = f"UPDATE users SET balance = {current_balance} WHERE id = '{self.user_id}'"
        self.db.make_query(query)


    def get_category_id(self, name):
        query = f"SELECT id FROM categories WHERE name = '{name}'"
        return self.db.select_data(query, 'one')[0]