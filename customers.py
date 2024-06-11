import sqlite3


class Customers:
    """
    Class representing a customer of a restaurant.
    """
    def __init__(self):
        """
        Initialize a customer instance.
        """
        self.conn = sqlite3.connect("pizza_restaurant.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Creates necessary tables if they do not exist yet.
        :return: None
        """
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
        """
        Adds a permanent customer to the database.
        :param first_name: (str) First name of the customer.
        :param last_name: (str) Last name of the customer.
        :param email: (str) Email of the customer.
        :param address: (str) The address of the customer.
        :return: Last row of the cursor position
        """
        self.cursor.execute('INSERT INTO customers (first_name, last_name, email, address) VALUES (?,?,?,?)',
                            (first_name, last_name, email, address))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_temp_customer(self, table_no, first_name, last_name):
        """
        Adds a permanent customer to the database.
        :param table_no: (int) Table no of the customer.
        :param first_name: (str) First name of the customer.
        :param last_name: (str) Last name of the customer.
        :return: Last row of the cursor position
        """
        self.cursor.execute('INSERT INTO temp_customers (table_no, first_name, last_name) VALUES (?,?,?)',
                            (table_no, first_name, last_name))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_table_no(self, customer_id):
        """
        Returns the table no of the customer who has the exact customer id with the parameter.
        :param customer_id: id of the customer.
        :return: Table no
        """
        table_no = self.cursor.execute('SELECT table_no FROM temp_customers WHERE id=?', (customer_id,)).fetchone()
        return table_no[0] if table_no else None
