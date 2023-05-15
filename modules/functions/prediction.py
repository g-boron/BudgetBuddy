import psycopg2
import pandas as pd
import math
from modules.database import database_connect


class Predictor:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = database_connect.DatabaseConnector()
        self.conn = psycopg2.connect(**self.db.params)
        self.cur = self.conn.cursor()

    def predict_budget(self):
        self.cur.execute(f"SELECT categories.name, EXTRACT(MONTH FROM expenses.add_date) AS month, EXTRACT(YEAR FROM expenses.add_date) AS year, SUM(expenses.amount) AS total_amount FROM expenses JOIN categories ON expenses.category_id = categories.id WHERE expenses.user_id={self.user_id} GROUP BY categories.name, month, year ORDER BY month")
        data = self.cur.fetchall()
        
        df = pd.DataFrame(data, columns=['category', 'month', 'year', 'total'])

        ent = df.loc[df['category']=='Entertainment', 'total'].mean()
        bills = df.loc[df['category']=='Bills', 'total'].mean()
        shop = df.loc[df['category']=='Shopping', 'total'].mean()
        subs = df.loc[df['category']=='Subscriptions', 'total'].mean()
        other = df.loc[df['category']=='Other', 'total'].mean()

        results = {'Entertainment': ent, 'Bills': bills, 'Shopping': shop, 'Subscriptions': subs, 'Other': other}
        
        for k, v in results.items():
            if math.isnan(v):
                results[k] = 0

        total = sum(results.values())
        results['Total'] = total

        return results
