from orders import *
from products import *
from customers import *
from error_handling import *
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


class SalesData:
    def __init__(self):
        self.db_path = 'pizza_restaurant.db'
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            raise

    def fetch_sales_data(self, period='Daily Sales'):
        if period == 'Daily Sales':
            query = '''
            SELECT order_taken_date AS OrderDate, SUM(total_price) AS TotalSales
            FROM finished_orders
            GROUP BY order_taken_date
            '''
        elif period == 'Weekly Sales':
            query = '''
            SELECT strftime('%Y-%W', order_taken_date) AS OrderDate, SUM(total_price) AS TotalSales
            FROM finished_orders
            GROUP BY strftime('%Y-%W', order_taken_date)
            '''
        elif period == 'Monthly Sales':
            query = '''
            SELECT strftime('%Y-%m', order_taken_date) AS OrderDate, SUM(total_price) AS TotalSales
            FROM finished_orders
            GROUP BY strftime('%Y-%m', order_taken_date)
            '''
        return pd.read_sql_query(query, self.conn)

    def fetch_customer_segment_data(self):
        query = '''
        SELECT 
            table_no AS TableNo,
            COUNT(*) AS NumberOfOrders,
            SUM(total_price) AS TotalSpent 
        FROM finished_orders
        JOIN temp_customers ON finished_orders.temp_customer_id = temp_customers.id
        GROUP BY table_no
        '''
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()

    @handle_errors
    def close_connection(self):
        self.conn.close()
        print("Database connection closed")

    @handle_errors
    def get_sales_summary(self, period):
        data = self.fetch_sales_data(period=period)
        if data.empty:
            return "No sales data available"
        summary = data.describe().to_string()
        return f"Sales Summary:\n{summary}"

    @handle_errors
    def plot_sales_trend(self, period):
        data = self.fetch_sales_data(period=period)
        if data.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No sales data available", ha='center', va='center', fontsize=12)
            return fig
        if period == 'Daily Sales':
            data['OrderDate'] = pd.to_datetime(data['OrderDate'])
        elif period == 'Weekly Sales':
            data['OrderDate'] = pd.to_datetime(data['OrderDate'] + '-0', format='%Y-%W-%w')
        elif period == 'Monthly Sales':
            data['OrderDate'] = pd.to_datetime(data['OrderDate'] + '-01')
        data = data.sort_values('OrderDate')
        fig, ax = plt.subplots()
        ax.plot(data['OrderDate'], data['TotalSales'])
        ax.set_title(f'{period} Trend')
        ax.set_xlabel('Order Date')
        ax.set_ylabel('Total Sales')
        plt.xticks(rotation=30)
        plt.tight_layout()
        return fig

    @handle_errors
    def get_customer_segments(self):
        data = self.fetch_customer_segment_data()
        if data.empty:
            return "No customer segment data available"
        segments = data.describe().to_string()
        return f"Customer Segments:\n{segments}"

    @handle_errors
    def plot_customer_segments(self):
        data = self.fetch_customer_segment_data()
        if data.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No customer segment data available", ha='center', va='center', fontsize=12)
            return fig
        fig, ax = plt.subplots()
        ax.bar(data['TableNo'], data['TotalSpent'])
        ax.set_title('Customer Segments')
        ax.set_xlabel('Table Number')
        ax.set_ylabel('Total Spent')
        plt.tight_layout()
        return fig

