import sqlite3


class Customers:
    def __init__(self):
        self.conn = sqlite3.connect("pizza_restaurant.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name VARCHAR(100) NOT NULL,
                  last_name VARCHAR(100) NOT NULL,
                  email VARCHAR(200) NOT NULL,
                  address TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_customers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  table_no TINYINT NOT NULL,
                  first_name VARCHAR(100),
                  last_name VARCHAR(100)
            )
        ''')
        self.conn.commit()

    def add_perm_customer(self, first_name, last_name, email, address):
        self.cursor.execute('INSERT INTO customers (first_name, last_name, email, address) VALUES (?,?,?,?)',
                            (first_name, last_name, email, address))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_temp_customer(self, table_no, first_name, last_name):
        self.cursor.execute('INSERT INTO temp_customers (table_no, first_name, last_name) VALUES (?,?,?)',
                            (table_no, first_name, last_name))
        self.conn.commit()
        return self.cursor.lastrowid
