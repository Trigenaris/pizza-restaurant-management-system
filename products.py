import sqlite3
from error_handling import *


class Product:
    def __init__(self, table_name, product_type):
        self.table_name = table_name
        self.product_type = product_type
        self.conn = sqlite3.connect("pizza_restaurant.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    # Main product table
    def create_table(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type INTEGER NOT NULL,
                name VARCHAR(200) NOT NULL,
                price REAL NOT NULL,
                ingredients TEXT 
            )
        ''')
        self.conn.commit()

    # Product related functions
    @handle_errors
    def add_product(self, name, price, ingredients):
        self.cursor.execute(f'''INSERT INTO {self.table_name} (type, name, price, ingredients) 
                            VALUES (?,?,?,?)''', (self.product_type, name, price, ingredients))
        self.conn.commit()
        print(f"Success! product {name} added")

    def remove_product(self, product_id):
        self.cursor.execute(f'DELETE FROM {self.table_name} WHERE id=?', (product_id,))
        self.conn.commit()
        print(f"Success! product deleted.")

    def update_product(self, product_id, name, price, ingredients):
        self.cursor.execute(f'UPDATE {self.table_name} SET name=?, price=?, ingredients=? WHERE id=?',
                            (name, price, ingredients, product_id))
        self.conn.commit()
        print(f"Success! id {product_id} has been updated.")

    def list_products(self):
        products = self.cursor.execute(f'SELECT id, {self.product_type}, name, price, ingredients FROM {self.table_name}').fetchall()
        return products

    def select_product(self, product_id):
        product = self.cursor.execute(f'''SELECT id, {self.product_type}, name, price, ingredients 
                                            FROM {self.table_name} WHERE id=?''', (product_id,)).fetchone()
        return product

    # Closing database connection
    def close_connection(self):
        self.conn.close()
        print("Database connection closed.")


# Product instances
class Pizza(Product):
    def __init__(self):
        super().__init__('pizzas', 0)


class Snack(Product):
    def __init__(self):
        super().__init__('snacks', 1)


class Drink(Product):
    def __init__(self):
        super().__init__('drinks', 2)
