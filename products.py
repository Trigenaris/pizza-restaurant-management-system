import sqlite3
from error_handling import *


class Product:
    """
    Class representing a product of a restaurant.
    """
    def __init__(self, table_name, product_type):
        """
        Initialize a product instance
        :param table_name (str): The table name which inherits from the product instance
        :param product_type (int): The product type as an integer type value.
        """
        self.table_name = table_name
        self.product_type = product_type
        self.conn = sqlite3.connect("pizza_restaurant.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    # Main product table
    def create_table(self):
        """
        Creates necessary tables if they do not exist yet.
        :return: None
        """
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
        """
        Adds a product in the database
        :param name: (str) Name of the product.
        :param price: (float) Price of the product.
        :param ingredients: (str) The ingredients of the product.
        :return: None
        """
        self.cursor.execute(f'''INSERT INTO {self.table_name} (type, name, price, ingredients) 
                            VALUES (?,?,?,?)''', (self.product_type, name, price, ingredients))
        self.conn.commit()
        print(f"Success! product {name} added")

    def remove_product(self, product_id):
        """
        Removes the product that refers to the product_id parameter
        :param product_id: (int) id of the product
        :return: None
        """
        self.cursor.execute(f'DELETE FROM {self.table_name} WHERE id=?', (product_id,))
        self.conn.commit()
        print(f"Success! product deleted.")

    def update_product(self, product_id, name, price, ingredients):
        """
        Updates the product that refers to the product_id parameter
        :param product_id: (int) id of the product.
        :param name: (str) New name of the product.
        :param price: (float) New price of the product.
        :param ingredients: (str) New ingredients of the product.
        :return: None
        """
        self.cursor.execute(f'UPDATE {self.table_name} SET name=?, price=?, ingredients=? WHERE id=?',
                            (name, price, ingredients, product_id))
        self.conn.commit()
        print(f"Success! id {product_id} has been updated.")

    def list_products(self):
        """
        Lists and returns all the products.
        :return: all the products.
        """
        products = self.cursor.execute(f'SELECT id, {self.product_type}, name, price, ingredients FROM {self.table_name}').fetchall()
        return products

    def select_product(self, product_id):
        """
        Selects and returns one specific product that matches the product_id parameter.
        :param product_id: id of the product.
        :return: referring product
        """
        product = self.cursor.execute(f'''SELECT id, {self.product_type}, name, price, ingredients 
                                            FROM {self.table_name} WHERE name=?''', (product_id,)).fetchone()
        return product

    # Closing database connection
    def close_connection(self):
        """
        Closes the database connection.
        :return: None
        """
        self.conn.close()
        print("Database connection closed.")


# Product instances
class Pizza(Product):
    """
    Class representing a pizza product which also inherits from the Product class.
    """
    def __init__(self):
        """
        Initialize a pizza product instance.
        """
        super().__init__('pizzas', 0)


class Snack(Product):
    """
    Class representing a snack product which also inherits from the Product class.
    """
    def __init__(self):
        """
        Initialize a snack product instance.
        """
        super().__init__('snacks', 1)


class Drink(Product):
    """
    Class representing a drink product which also inherits from the Product class.
    """
    def __init__(self):
        """
        Initialize a drink product instance.
        """
        super().__init__('drinks', 2)
