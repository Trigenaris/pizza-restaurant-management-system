import sqlite3
from datetime import datetime
from customers import *
from products import *


class OrderDetails:
    """
    Class representing the order details of a restaurant.
    """
    def __init__(self):
        """
        Initialize an order details instance.
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
            CREATE TABLE IF NOT EXISTS order_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                item_id INTEGER,
                item_type INTEGER,
                item_name VARCHAR(200),
                quantity INTEGER,
                FOREIGN KEY (order_id) REFERENCES Orders(id),
                FOREIGN KEY (item_type) REFERENCES Products(type),
                FOREIGN KEY (item_id) REFERENCES Products(id)
            )
        ''')

    def add_order_details(self, order_id, item_type, item_id, item_name, quantity):
        """
        Adds the order details to which refers to the current order_id parameter.
        :param order_id: id of the order that is referenced from Orders class.
        :param item_type: item type of the product that is referenced from Product class.
        :param item_id: id of the product that is referenced from Product class.
        :param item_name: name of the product that is referenced from Product class.
        :param quantity: quantity of the ordered product.
        :return: None
        """
        self.cursor.execute('INSERT INTO order_details (order_id, item_id, item_type, item_name, quantity) VALUES (?,?,?,?,?)',
                            (order_id, item_type, item_id, item_name, quantity))
        self.conn.commit()

    # For now, this function is obsolete
    def get_order_items(self, order_id):
        self.cursor.execute('''SELECT 
                                o.id,
                                P1.type,
                                P2.name,
                                od.quantity
                            FROM order_details AS od
                            JOIN Products AS P1 ON item_type = P1.type
                            JOIN Products AS P2 ON item_id = P2.id 
                            JOIN Orders AS O ON order_id = O.id
                            WHERE od.order_id=?
                            ''', (order_id,))
        order_items = self.cursor.fetchall()
        return order_items


class Orders:
    """
    Class representing the orders of a restaurant.
    """
    def __init__(self, table_name):
        """
        Initialize an orders instance.
        :param table_name (str): The table name which inherits from the orders instance
        """
        self.table_name = table_name
        self.conn = sqlite3.connect("pizza_restaurant.db")
        self.cursor = self.conn.cursor()
        self.order_details = OrderDetails()
        self.create_table()
        self.current_time = datetime.now()

    # Main order table
    def create_table(self):
        """
        Creates necessary tables if they do not exist yet.
        :return: None
        """
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temp_customer_id INTEGER,
                customer_id INTEGER,
                total_price REAL NOT NULL,
                order_taken_date DATETIME NOT NULL,
                order_taken_hour DATETIME NOT NULL,
                order_prepared_hour DATETIME,
                FOREIGN KEY (temp_customer_id) REFERENCES temp_customers(id)
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        self.conn.commit()

    def take_order(self, customer_type, customer_id, items, total_price):
        """
        Takes an order information given from the customer and insert the data to the related table.
        :param customer_type: (int) Type of the customer. (0 is temp_customer and 1 is perm_customer.)
        :param customer_id: (id) id of the customer.
        :param items: (iterable) Ordered items
        :param total_price: (float) Total price of the order. (Currently obsolete parameter)
        :return: None
        """
        total_price = 0  # Currently total_price is defined in the function with a default 0 value.
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        if customer_type == 0:  # temp_customers
            for item in items:
                item_id, item_type, item_name, item_price, quantity = item
                price = self.get_product_price(item_type, item_id)
                total_price += float(price) * int(quantity)
                item_name = self.get_product_name(item_type, item_id)

            self.cursor.execute(f'''INSERT INTO {self.table_name} (
                temp_customer_id, total_price, order_taken_date, order_taken_hour) VALUES (?,?,?,?)''',
                                (customer_id, total_price, current_date, current_time))
            self.conn.commit()
            order_id = self.cursor.lastrowid

            for item in items:
                item_id, item_type, item_name, item_price, quantity = item
                item_name = self.get_product_name(item_type, item_id)
                self.order_details.add_order_details(order_id, item_id, item_type, item_name, quantity)

        else:  # perm_customers
            for item in items:
                item_id, item_type, item_name, item_price, quantity = item
                price = self.get_product_price(item_type, item_id)
                total_price += float(price) * int(quantity)
                item_name = self.get_product_name(item_type, item_id)

            self.cursor.execute(f'''INSERT INTO {self.table_name} (
                customer_id, total_price, order_taken_date, order_taken_hour) VALUES (?,?,?,?)''',
                                (customer_id, total_price, current_date, current_time))
            self.conn.commit()
            order_id = self.cursor.lastrowid

            for item in items:
                item_id, item_type, item_name, item_price, quantity = item
                item_name = self.get_product_name(item_type, item_id)
                self.order_details.add_order_details(order_id, item_id, item_type, item_name, quantity)
            self.conn.commit()

    def get_active_orders(self):
        """
        Returns the orders and the details of the orders via a new query (order_details is used in the query with JOIN)
        :return: All the data which responds to the query.
        """
        self.cursor.execute(f'''
        SELECT 
            o.id,
            o.temp_customer_id,
            o.total_price,
            o.order_taken_date,
            o.order_taken_hour,
            GROUP_CONCAT(order_details.item_name || ' (' || order_details.quantity || ')', ', ') AS items
        FROM {self.table_name} AS o
        JOIN order_details ON o.id = order_details.order_id
        GROUP BY o.id, o.temp_customer_id, o.total_price, o.order_taken_date, o.order_taken_hour''')
        print("Active Orders")
        return self.cursor.fetchall()

    def get_finished_orders(self):
        """
        Returns the orders and the details of the orders via a new query (order_details is used in the query with JOIN)
        :return: All the data which responds to the query.
        """
        self.cursor.execute(f'''
        SELECT 
            o.id,
            o.temp_customer_id,
            o.total_price,
            o.order_taken_date,
            o.order_taken_hour,
            o.order_prepared_hour,
            GROUP_CONCAT(order_details.item_name || ' (' || order_details.quantity || ')', ', ') AS items
        FROM {self.table_name} AS o
        JOIN order_details ON o.id = order_details.order_id
        GROUP BY o.id, o.temp_customer_id, o.total_price, o.order_taken_date, o.order_taken_hour, o.order_prepared_hour''')
        print("Finished Orders")
        return self.cursor.fetchall()

    def cancel_order(self, order_id):
        """
        Cancels and removes the selected order from the database.
        :param order_id: id of the order.
        :return: None
        """
        self.cursor.execute(f"DELETE FROM order_details WHERE order_id = ?", (order_id,))
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (order_id,))
        self.conn.commit()

    def get_product_price(self, item_type, product_id):
        """
        Gets and returns the price of the product which has the same product_id.
        :param item_type: (int) Type of the product.
        :param product_id: (int) id of the product.
        :return: (float) Price of the product.
        """
        table_name = 'pizzas' if item_type == 0 else 'snacks' if item_type == 1 else 'drinks'
        price = self.cursor.execute(f'SELECT price FROM {table_name} WHERE id=?', (product_id,)).fetchone()
        return price[0] if price else 0

    def get_product_name(self, item_type, product_id):
        """
        Gets and returns the name of the product which has the same product_id.
        :param item_type: (int) Type of the product.
        :param product_id: (int) id of the product.
        :return: (str) Name of the product.
        """
        table_name = 'pizzas' if item_type == 0 else 'snacks' if item_type == 1 else 'drinks'
        name = self.cursor.execute(f'SELECT name FROM {table_name} WHERE id=?', (product_id,)).fetchone()
        return name[0] if name else 0

    # For now, this function is obsolete
    def get_order_details(self, order_id):
        return self.order_details.get_order_items(order_id)


class ActiveOrders(Orders):
    """
    Class representing an active order which also inherits from the Orders class.
    """
    def __init__(self):
        """
        Initialize an active order instance.
        """
        super().__init__('active_orders')

    def finished_order(self, order_id):
        """
        Transfers an active order to the finished orders table and deletes it from the active orders table.
        :param order_id: (int) id of the order
        :return: Boolean
        """
        prepared_time = datetime.now().strftime('%H:%M:%S')
        if order_id:
            try:
                self.cursor.execute(f'UPDATE active_orders SET order_prepared_hour=? WHERE id=?',
                                    (prepared_time, order_id))

                self.cursor.execute(f'INSERT INTO finished_orders SELECT * FROM active_orders WHERE id=?', (order_id,))
                self.cursor.execute(f"DELETE FROM active_orders WHERE id = ?", (order_id,))
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Error: {e}")
                # To prevent data loss
                self.conn.rollback()
                return False
        else:
            print("Error! Wrong order id!")
            return False


class FinishedOrders(Orders):
    """
    Class representing a finished order which also inherits from the Orders class.
    """
    def __init__(self):
        """
        Initialize a finished order instance.
        """
        super().__init__('finished_orders')


# Obsolete subclass of the Orders class
class CanceledOrders(Orders):
    def __init__(self):
        super().__init__('canceled_orders')
