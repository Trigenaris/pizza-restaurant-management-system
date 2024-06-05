import sqlite3
from datetime import datetime
from customers import *
from products import *


class OrderDetails:
    def __init__(self):
        self.conn = sqlite3.connect("pizza_restaurant.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                item_type INTEGER,
                item_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (order_id) REFERENCES Orders(id),
                FOREIGN KEY (item_type) REFERENCES Products(type),
                FOREIGN KEY (item_id) REFERENCES Products(id)
            )
        ''')

    def add_order_details(self, order_id, item_type, item_id, quantity):
        self.cursor.execute('INSERT INTO order_details (order_id, item_type, item_id, quantity) VALUES (?,?,?,?)',
                            (order_id, item_type, item_id, quantity))
        self.conn.commit()

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

    def delete_order_details(self, order_id):
        self.cursor.execute('DELETE FROM order_details WHERE order_id = ?', (order_id,))
        self.conn.commit()


class Orders:
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = sqlite3.connect("pizza_restaurant.db")
        self.cursor = self.conn.cursor()
        self.order_details = OrderDetails()
        self.create_table()
        self.current_time = datetime.now()

    # Main order table
    def create_table(self):
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

    def take_order(self, customer_type, customer_id, items):
        total_price = 0
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        if customer_type == 0:  # temp_customers
            for item in items:
                item_id, item_type, quantity = item
                price = self.get_product_price(item_type, item_id)
                total_price += price * quantity

            self.cursor.execute(f'''INSERT INTO {self.table_name} (
                temp_customer_id, total_price, order_taken_date, order_taken_hour) VALUES (?,?,?,?)''',
                                (customer_id, total_price, current_date, current_time))
            self.conn.commit()
            order_id = self.cursor.lastrowid

            for item in items:
                item_id, item_type, quantity = item
                self.order_details.add_order_details(order_id, item_id, item_type, quantity)
        else:
            for item in items:
                item_id, item_type, quantity = item
                price = self.get_product_price(item_type, item_id)
                total_price += price * quantity

            self.cursor.execute(f'''INSERT INTO {self.table_name} (
                customer_id, total_price, order_taken_date, order_taken_hour) VALUES (?,?,?,?)''',
                                (customer_id, total_price, current_date, current_time))
            self.conn.commit()
            order_id = self.cursor.lastrowid

            for item in items:
                item_id, item_type, quantity = item
                self.order_details.add_order_details(order_id, item_id, item_type, quantity)
            self.conn.commit()

    # def prepared_order(self, order_id):
    #     prepared_time = self.current_time.time()
    #     if order_id:
    #         self.cursor.execute(f'UPDATE {self.table_name} SET order_prepared_hour=? WHERE id=?',
    #                             (prepared_time, order_id))
    #         self.conn.commit()
    #         return True
    #     else:
    #         print("Error! Wrong order id!")
    #         return False

    def finished_order(self, order_id):
        prepared_time = self.current_time.time()
        if order_id:
            self.cursor.execute(f'UPDATE {self.table_name} SET order_prepared_hour=? WHERE id=?',
                                (prepared_time, order_id))
            self.conn.commit()
            # Move the order to the finished_orders table
            self.cursor.execute(f'INSERT INTO finished_orders SELECT * FROM {self.table_name} WHERE id=?', (order_id,))
            self.conn.commit()
            return True
        else:
            print("Error! Wrong order id!")
            return False

    def copy_order(self, order_id):
        order_details = self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE id=?', (order_id,)).fetchone()
        return order_details[1:] if order_details else 0

    def insert_order(self, order_details):
        self.cursor.execute(f'''INSERT INTO {self.table_name} (
        temp_customer_id, pizza_id, snack_id, drink_id, pizza_quantity, snack_quantity, drink_quantity, total_price,
        order_taken_date, order_taken_hour) VALUES (?,?,?,?,?,?,?,?,?)''', (order_details,))
        self.conn.commit()

    def delete_order(self, order_id):
        self.cursor.execute(f'DELETE FROM {self.table_name} WHERE id=?', (order_id,))
        self.conn.commit()

    def get_product_price(self, item_type, product_id):
        table_name = 'pizzas' if item_type == 0 else 'snacks' if item_type == 1 else 'drinks'
        price = self.cursor.execute(f'SELECT price FROM {table_name} WHERE id=?', (product_id,)).fetchone()
        return price[0] if price else 0

    def get_product_name(self, item_type, product_id):
        table_name = 'pizzas' if item_type == 0 else 'snacks' if item_type == 1 else 'drinks'
        name = self.cursor.execute(f'SELECT name FROM {table_name} WHERE id=?', (product_id,)).fetchone()
        return name[0] if name else 0

    def get_order_details(self, order_id):
        return self.order_details.get_order_items(order_id)


class ActiveOrders(Orders):
    def __init__(self):
        super().__init__('active_orders')


class FinishedOrders(Orders):
    def __init__(self):
        super().__init__('finished_orders')


class CanceledOrders(Orders):
    def __init__(self):
        super().__init__('canceled_orders')
