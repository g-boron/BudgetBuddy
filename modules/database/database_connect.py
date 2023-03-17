import psycopg2
from configparser import ConfigParser
import os


class DatabaseConnector:
    def __init__(self, filename='database.ini', section='postgresql'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'database.ini')
        self.params = self._config(config_path, section)

    
    def _config(self, filename, section):
        parser = ConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f'Section {section} not found in the {filename} file.')

        return db

    
    def make_query(self, query):
        '''
        jak chce sie uzyc inserta do zarejestrowania to trzeba wpisac tak:
        from modules.database import database_connect

        db = database_connect.DatabaseConnector() <- utworzenie obiektu klasy
        query = f"INSERT INTO users (username, password, email) VALUES('{usernameEntry}', '{passwordEntry}', '{emailEntry}')" <- polecenie do inserta
        db.insert_data(query) <- wykonanie inserta

        lub do usuwania:
        db = database_connect.DatabaseConnector()
        query = 'DELETE FROM users where id=11'
        db.insert_data(query)
        '''
        conn = None

        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            print('Inserted successfully')
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    
    def select_data(self, query, fetch='all'):
        '''
        uzywanie:
        db = database_connect.DatabaseConnector()
        query = 'SELECT username, password, email from users'
        records = db.select_data(query)

        for row in records:
            print(row)

        jak sie chce zwrocic tylko 1 rekord to fetch = 'one':
        db = DatabaseConnector()
        query = f"SELECT balance FROM users WHERE username = '{username}'"
        self.balance = db.select_data(query, 'one')
        '''
        conn = None

        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            cur.execute(query)
            if fetch == 'one':
                records = cur.fetchone()
            else:
                records = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                return records
