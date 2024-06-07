import sqlite3
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime

import custom_messageboxes
from customers import *
from products import *
from orders import *
from error_handling import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from custom_messageboxes import *
from dashboard import *

# Constant values
PADX = 5
PADY = 5
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

total_price = 0


class GUI:
    def __init__(self, window):
        # main window setup
        self.window = window
        self.window.title("Crazy Pizza Restaurant Management System")
        self.display_width = window.winfo_screenwidth()
        self.display_height = window.winfo_screenheight()
        self.left = int(self.display_width / 2 - (WINDOW_WIDTH / 2))
        self.top = int(self.display_height / 2 - (WINDOW_HEIGHT / 2))
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{self.left}+{self.top}")
        self.window.config(padx=PADX*2, pady=PADY*2)
        self.window.minsize(int(WINDOW_WIDTH/1.25), int(WINDOW_HEIGHT/1.25))

        # login screen
        self.login_frame = ttk.Frame(window)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ttk.Label(self.login_frame, text="Welcome to Crazy Pizza!", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=PADX, pady=PADY)

        self.login_canvas = tk.Canvas(self.login_frame, width=200, height=200)
        self.login_canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=PADX, pady=PADY)
        self.logo_image = tk.PhotoImage(file="crazy_logo.png")
        self.login_canvas.create_image(100, 100, image=self.logo_image)

        self.user_label = ttk.Label(self.login_frame, text="User: ")
        self.user_label.grid(row=2, column=0, sticky="nsew", padx=PADX, pady=PADY)
        self.user_tuple = ("Manager", "Waiter", "Chef")
        self.user_string = tk.StringVar(value=self.user_tuple[0])
        self.combobox_product = ttk.Combobox(self.login_frame, textvariable=self.user_string)
        self.combobox_product['values'] = self.user_tuple
        self.combobox_product.grid(row=2, column=1, sticky="nsew", padx=PADX, pady=PADY)

        self.password_label = ttk.Label(self.login_frame, text="Password: ")
        self.password_label.grid(row=3, column=0, sticky="nsew", padx=PADX, pady=PADY)
        self.password_string = tk.StringVar(value="")
        self.password_entry = ttk.Entry(self.login_frame, width=30, textvariable=self.password_string, show="*")
        self.password_entry.grid(row=3, column=1, sticky="nsew", padx=PADX, pady=PADY)
        self.password = "123456"

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login_process)
        self.login_button.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=PADX, pady=PADY)

        self.grip = ttk.Sizegrip(window)
        self.grip.place(relx=1.0, rely=1.0, anchor="se")

        # Storing images for each tab
        self.manager_images = []
        self.waiter_images = []
        self.chef_images = []

        # database instances
        self.pizzas = Pizza()
        self.snacks = Snack()
        self.drinks = Drink()
        self.active_orders = ActiveOrders()
        self.finished_orders = FinishedOrders()
        self.canceled_orders = CanceledOrders()
        self.order_details = OrderDetails()
        self.customers = Customers()
        self.items = []

    def login_process(self):
        user = self.user_string.get()
        password = self.password_string.get()
        if user == "Manager" and password == self.password:
            self.manager_menu()
        elif user == "Waiter":
            self.waiter_menu()
        elif user == "Chef":
            self.chef_menu()
        else:
            custom_showerror(self.window, title="Error!", message="Oops! \nInvalid username or password.")
            # messagebox.showerror(title="Error!", message="Oops! \nInvalid username or password.")

    def manager_menu(self):
        # Manager Window Setup
        manager_window = tk.Toplevel(self.window)
        manager_window.title("Crazy Pizza Management")

        self.left = int(self.display_width / 2 - (WINDOW_WIDTH / 2))
        self.top = int(self.display_height / 2 - (WINDOW_HEIGHT / 2))
        manager_window.geometry(f"{int(WINDOW_WIDTH*1.5)}x{WINDOW_HEIGHT}+{self.left}+{self.top}")
        manager_window.config(padx=PADX, pady=PADY)
        manager_window.minsize(int(WINDOW_WIDTH*1.5 / 1.25), int(WINDOW_HEIGHT / 1.25))

        # Multiple tabs for the manager window
        notebook = ttk.Notebook(manager_window)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)
        notebook.add(tab1, text="Menu Management")
        notebook.add(tab2, text="Active Orders")
        notebook.add(tab3, text="Finished Orders")
        notebook.add(tab4, text="Analysis")
        notebook.pack(fill=tk.BOTH)

        # First tab frames
        left_frame1 = ttk.Frame(tab1, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame1.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame1 = ttk.Frame(tab1, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame1.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame1.pack_propagate(False)

        self.display_manager_logo(left_frame1)

        # Second tab frames
        left_frame2 = ttk.Frame(tab2, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame2.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame2 = ttk.Frame(tab2, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame2.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame2.pack_propagate(False)

        self.display_manager_logo(left_frame2)

        # Third tab frames
        left_frame3 = ttk.Frame(tab3, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame3.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame3 = ttk.Frame(tab3, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame3.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame3.pack_propagate(False)

        self.display_manager_logo(left_frame3)

        # Fourth tab frames
        left_frame4 = ttk.Frame(tab4, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame4.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame4 = ttk.Frame(tab4, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame4.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame4.pack_propagate(False)

        self.display_manager_logo(left_frame4)

        show_menu_button = ttk.Button(left_frame1, text="Show Menu", command=lambda: show_menu(right_frame1))
        show_menu_button.grid(row=1, column=1, padx=PADX, pady=PADY)
        add_product_button = ttk.Button(left_frame1, text="New Product", command=self.add_product)
        add_product_button.grid(row=2, column=1, padx=PADX, pady=PADY)
        remove_product_button = ttk.Button(left_frame1, text="Remove Product", command=lambda: self.remove_product(self.tree_menu))
        remove_product_button.grid(row=3, column=1, padx=PADX, pady=PADY)
        update_product_button = ttk.Button(left_frame1, text="Update Product", command=lambda: self.update_product(self.tree_menu))
        update_product_button.grid(row=4, column=1, padx=PADX, pady=PADY)

        @handle_errors
        def show_active_orders(frame):
            self.cleaning_frame(frame)
            tree_active_orders = ttk.Treeview(frame, show="headings", selectmode="browse")
            tree_active_orders["columns"] = (
                "Order ID", "Table No", "Total Price", "Order Date", "Order Hour", "Items")
            tree_active_orders.column("Order ID", anchor="center", width=80)
            tree_active_orders.column("Table No", anchor="center", width=100)
            tree_active_orders.column("Total Price", anchor="center", width=100)
            tree_active_orders.column("Order Date", anchor="center", width=100)
            tree_active_orders.column("Order Hour", anchor="center", width=100)
            tree_active_orders.column("Items", anchor="center", width=300)
            tree_active_orders.heading("Order ID", text="Order ID")
            tree_active_orders.heading("Table No", text="Table No")
            tree_active_orders.heading("Total Price", text="Total Price")
            tree_active_orders.heading("Order Date", text="Order Date")
            tree_active_orders.heading("Order Hour", text="Order Hour")
            tree_active_orders.heading("Items", text="Items")
            tree_active_orders.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            active_orders = self.active_orders.get_active_orders()
            print(f"Active Orders: {active_orders}")
            for order in active_orders:
                table_no = self.customers.get_table_no(order[1])
                print(f"Inserting order: {order}")
                order_with_table = (order[0], table_no, order[2], order[3], order[4], order[5])
                tree_active_orders.insert("", "end", values=order_with_table)

        @handle_errors
        def show_finished_orders(frame):
            self.cleaning_frame(frame)
            tree_finished_orders = ttk.Treeview(frame, show="headings", selectmode="browse")
            tree_finished_orders["columns"] = (
                "Order ID", "Table No", "Total Price", "Order Date", "Order Hour", "Prepared Hour", "Items")
            tree_finished_orders.column("Order ID", anchor="center", width=80)
            tree_finished_orders.column("Table No", anchor="center", width=100)
            tree_finished_orders.column("Total Price", anchor="center", width=100)
            tree_finished_orders.column("Order Date", anchor="center", width=100)
            tree_finished_orders.column("Order Hour", anchor="center", width=100)
            tree_finished_orders.column("Prepared Hour", anchor="center", width=100)
            tree_finished_orders.column("Items", anchor="center", width=300)
            tree_finished_orders.heading("Order ID", text="Order ID")
            tree_finished_orders.heading("Table No", text="Table No")
            tree_finished_orders.heading("Total Price", text="Total Price")
            tree_finished_orders.heading("Order Date", text="Order Date")
            tree_finished_orders.heading("Order Hour", text="Order Hour")
            tree_finished_orders.heading("Prepared Hour", text="Prepared Hour")
            tree_finished_orders.heading("Items", text="Items")
            tree_finished_orders.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            finished_orders = self.finished_orders.get_finished_orders()
            for order in finished_orders:
                table_no = self.customers.get_table_no(order[1])
                print(f"Inserting order: {order}")
                order_with_table = (order[0], table_no, order[2], order[3], order[4], order[5], order[6])
                tree_finished_orders.insert("", "end", values=order_with_table)

        # Analysis Widgets
        analysis_type_label = tk.Label(left_frame4, text="Select Analysis Type:")
        analysis_type_label.grid(row=1, column=0, padx=PADX, pady=PADY)

        analysis_type_combobox = ttk.Combobox(left_frame4, values=[
            "Sales Summary", "Sales Trend", "Customer Segments", "Customer Segments Plot"
        ])
        analysis_type_combobox.grid(row=1, column=1, padx=PADX, pady=PADY)
        analysis_type_combobox.current(0)

        analysis_button = ttk.Button(left_frame4, text="Show Analysis",
                                     command=lambda: show_analysis(right_frame4, analysis_type_combobox.get()))
        analysis_button.grid(row=2, column=1, columnspan=2, pady=10)

        # Analysis Functions
        @handle_errors
        def show_analysis(frame, analysis_type):
            for widget in frame.winfo_children():
                if widget != analysis_type_label and widget != analysis_type_combobox and widget != analysis_button:
                    widget.destroy()

            sales_data = SalesData()

            if analysis_type == "Sales Summary":
                summary = sales_data.get_sales_summary()
                text_widget = tk.Text(frame, wrap='word')
                text_widget.pack(expand=True, fill='both')
                text_widget.insert(tk.END, summary)
            elif analysis_type == "Sales Trend":
                fig = sales_data.plot_sales_trend()
                canvas = FigureCanvasTkAgg(fig, frame)
                canvas.draw()
                canvas.get_tk_widget().pack(expand=True, fill='both')
            elif analysis_type == "Customer Segments":
                segments = sales_data.get_customer_segments()
                text_widget = tk.Text(frame, wrap='word')
                text_widget.pack(expand=True, fill='both')
                text_widget.insert(tk.END, segments)
            elif analysis_type == "Customer Segments Plot":
                fig = sales_data.plot_customer_segments()
                canvas = FigureCanvasTkAgg(fig, frame)
                canvas.draw()
                canvas.get_tk_widget().pack(expand=True, fill='both')

            sales_data.close_connection()

        # Placing grip at the corner
        grip = ttk.Sizegrip(manager_window)
        grip.place(relx=1.0, rely=1.0, anchor="se")

        @handle_errors
        def show_menu(frame):
            self.cleaning_frame(frame)
            self.tree_menu = ttk.Treeview(frame, show="headings", selectmode="browse")
            self.tree_menu["columns"] = ("ID", "Type", "Name", "Price", "Ingredients")
            self.tree_menu.column("ID", anchor="center", width=25)
            self.tree_menu.column("Type", anchor="center", width=50)
            self.tree_menu.column("Name", anchor="center", width=200)
            self.tree_menu.column("Price", anchor="center", width=50)
            self.tree_menu.column("Ingredients", anchor="center", width=400)
            self.tree_menu.heading("ID", text="ID")
            self.tree_menu.heading("Type", text="Type")
            self.tree_menu.heading("Name", text="Name")
            self.tree_menu.heading("Price", text="Price")
            self.tree_menu.heading("Ingredients", text="Ingredients")
            self.tree_menu.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            self.pizza = Pizza()
            self.snack = Snack()
            self.drink = Drink()

            pizzas = self.pizza.list_products()
            snacks = self.snack.list_products()
            drinks = self.drink.list_products()

            for pizza in pizzas:
                self.tree_menu.insert("", "end", values=(pizza[0], "Pizza", pizza[2], pizza[3], pizza[4]))

            for snack in snacks:
                self.tree_menu.insert("", "end", values=(snack[0], "Snack", snack[2], snack[3], snack[4]))

            for drink in drinks:
                self.tree_menu.insert("", "end", values=(drink[0], "Drink", drink[2], drink[3], drink[4]))

        # Second tab buttons
        active_orders_button = ttk.Button(left_frame2, text="Show Active Orders",
                                          command=lambda: show_active_orders(right_frame2))
        active_orders_button.grid(row=1, column=1, padx=PADX, pady=PADY)

        # Third tab buttons
        finished_orders_button = ttk.Button(left_frame3, text="Show Finished Orders",
                                            command=lambda: show_finished_orders(right_frame3))
        finished_orders_button.grid(row=1, column=1, padx=PADX, pady=PADY*3)

        notebook.bind("<<NotebookTabChanged>>",
                      lambda event: show_active_orders(right_frame2) if notebook.index("current") == 1 else None)
        notebook.bind("<<NotebookTabChanged>>",
                      lambda event: show_finished_orders(right_frame3) if notebook.index("current") == 2 else None)

    # Product management functions
    @handle_errors
    def add_product(self):
        add_product_window = tk.Toplevel(self.window)
        add_product_window.title("New Product")
        add_product_window.geometry("500x400")
        add_product_window.resizable(False, False)

        product_type_label = ttk.Label(add_product_window, text="Product Type: ")
        product_type_label.grid(row=0, column=0, sticky="nsew", padx=PADX, pady=PADY)
        product_tuple = ("Pizza", "Snack", "Drink")
        product_string = tk.StringVar(value=product_tuple[0])
        combobox_product = ttk.Combobox(add_product_window, textvariable=product_string)
        combobox_product['values'] = product_tuple
        combobox_product.grid(row=0, column=1, sticky="nsew", padx=PADX, pady=PADY)

        product_name_label = ttk.Label(add_product_window, text="Product Name: ")
        product_name_label.grid(row=1, column=0, sticky="nsew", padx=PADX, pady=PADY)
        product_name_entry = ttk.Entry(add_product_window, width=30)
        product_name_entry.grid(row=1, column=1, sticky="nsew", padx=PADX, pady=PADY)

        product_price_label = ttk.Label(add_product_window, text="Product Price: ")
        product_price_label.grid(row=2, column=0, sticky="nsew", padx=PADX, pady=PADY)
        product_price_entry = ttk.Entry(add_product_window, width=30)
        product_price_entry.grid(row=2, column=1, sticky="nsew", padx=PADX, pady=PADY)

        product_ingredients_label = ttk.Label(add_product_window, text="Ingredients: ")
        product_ingredients_label.grid(row=3, column=0, sticky="nsew", padx=PADX, pady=PADY)
        product_ingredients_entry = tk.Text(add_product_window, width=30, height=15)
        product_ingredients_entry.grid(row=3, column=1, sticky="nsew", padx=PADX, pady=PADY)

        @handle_errors
        def adding_product():
            product_type = product_string.get()
            product_name = product_name_entry.get()
            product_price = float(product_price_entry.get())
            product_ingredients = product_ingredients_entry.get("1.0", tk.END).strip()

            if product_type and product_name and product_price:

                if product_type == "Pizza":
                    self.pizzas.add_product(product_name, product_price, product_ingredients)
                elif product_type == "Snack":
                    self.snacks.add_product(product_name, product_price, product_ingredients)
                elif product_type == "Drink":
                    self.drinks.add_product(product_name, product_price, product_ingredients)
                else:
                    messagebox.showerror(title="Error!", message="Oops! \nInvalid product type.")

            else:
                messagebox.showwarning(title="Warning!", message="Please fill the Product Name and the Product Price.")

        adding_product_button = ttk.Button(add_product_window, text="Add Product", command=adding_product)
        adding_product_button.grid(row=4, column=0, columnspan=2, pady=PADY)

    @handle_errors
    def update_product(self, tree_menu):
        selected_item = tree_menu.selection()
        if not selected_item:
            messagebox.showwarning(title="Warning!", message="You haven't selected any product from the menu.")
            return

        update_product_window = tk.Toplevel(self.window)
        update_product_window.title("Update Product")
        update_product_window.geometry("500x400")
        update_product_window.resizable(False, False)

        item_values = tree_menu.item(selected_item)["values"]
        item_id = item_values[0]
        item_type = item_values[1]
        old_name = item_values[2]
        print(f"old name: {old_name}")
        old_price = item_values[3]
        print(f"old price: {old_price}")
        old_ingredients = item_values[4]

        product_name_label = ttk.Label(update_product_window, text="New Product Name: ")
        product_name_label.grid(row=1, column=0, sticky="nsew", padx=PADX, pady=PADY)
        product_name_entry = ttk.Entry(update_product_window, width=30)
        product_name_entry.insert(tk.END, old_name)
        product_name_entry.grid(row=1, column=1, sticky="nsew", padx=PADX, pady=PADY)

        product_price_label = ttk.Label(update_product_window, text="New Product Price: ")
        product_price_label.grid(row=2, column=0, sticky="nsew", padx=PADX, pady=PADY)
        product_price_entry = ttk.Entry(update_product_window, width=30)
        product_price_entry.insert(tk.END, old_price)
        product_price_entry.grid(row=2, column=1, sticky="nsew", padx=PADX, pady=PADY)

        product_ingredients_label = ttk.Label(update_product_window, text="New Ingredients: ")
        product_ingredients_label.grid(row=3, column=0, sticky="nsew", padx=PADX, pady=PADY)
        product_ingredients_entry = tk.Text(update_product_window, width=30, height=15)
        product_ingredients_entry.insert(tk.END, old_ingredients)
        product_ingredients_entry.grid(row=3, column=1, sticky="nsew", padx=PADX, pady=PADY)

        @handle_errors
        def updating_product():
            updated_name = product_name_entry.get()
            updated_price = float(product_price_entry.get())
            updated_ingredients = product_ingredients_entry.get("1.0", tk.END)
            if updated_name and updated_price:
                if item_type == "Pizza":
                    self.pizzas.update_product(item_id, updated_name, updated_price, updated_ingredients)
                    tree_menu.item(selected_item, values=(item_id, updated_name, updated_price, updated_ingredients))
                    messagebox.showinfo(title="Success!", message="Product updated successfully!")
                    update_product_window.destroy()
                elif item_type == "Snack":
                    self.snacks.update_product(item_id, updated_name, updated_price, updated_ingredients)
                    tree_menu.item(selected_item, values=(item_id, updated_name, updated_price, updated_ingredients))
                    messagebox.showinfo(title="Success!", message="Product updated successfully!")
                    update_product_window.destroy()
                elif item_type == "Drink":
                    self.drinks.update_product(item_id, updated_name, updated_price, updated_ingredients)
                    tree_menu.item(selected_item, values=(item_id, updated_name, updated_price, updated_ingredients))
                    messagebox.showinfo(title="Success!", message="Product updated successfully!")
                    update_product_window.destroy()
            else:
                messagebox.showwarning(title="Warning!", message="Please fill the New name and the New price.")

        updating_product_button = ttk.Button(update_product_window, text="Update Product", command=updating_product)
        updating_product_button.grid(row=4, column=0, columnspan=2, pady=PADY)

    @handle_errors
    def remove_product(self, tree_menu):
        selected_item = tree_menu.selection()
        if not selected_item:
            messagebox.showwarning(title="Warning!", message="You haven't selected any product from the menu.")
            return

        remove_product_window = tk.Toplevel(self.window)
        remove_product_window.title("Remove Product")
        remove_product_window.geometry("350x200")
        remove_product_window.resizable(False, False)

        item_values = tree_menu.item(selected_item)["values"]
        item_id = item_values[0]
        item_type = item_values[1]
        name = item_values[2]
        price = item_values[3]

        remove_product_label = ttk.Label(remove_product_window, text=f'''
        The product you selected to remove is:
                Product ID: {item_id}
                Product Type: {item_type}
                Product Name: {name}
                Product Price: {price}
        ''')
        remove_product_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=PADX, pady=PADY)

        @handle_errors
        def removing_product():
            if messagebox.askyesno(title="Remove Product", message="Are you sure to remove this product?"):
                if item_type == "Pizza":
                    self.pizzas.remove_product(item_id)
                    messagebox.showinfo(title="Success!", message="Product removed successfully!")
                    remove_product_window.destroy()
                elif item_type == "Snack":
                    self.snacks.remove_product(item_id)
                    messagebox.showinfo(title="Success!", message="Product removed successfully!")
                    remove_product_window.destroy()
                elif item_type == "Drink":
                    self.drinks.remove_product(item_id)
                    messagebox.showinfo(title="Success!", message="Product removed successfully!")
                    remove_product_window.destroy()

        remove_product_button = ttk.Button(remove_product_window, text="Remove Product", command=removing_product)
        remove_product_button.grid(row=1, column=0, padx=PADX, pady=PADY*2)

        cancel_button = ttk.Button(remove_product_window, text="Cancel", command=remove_product_window.destroy)
        cancel_button.grid(row=1, column=1, padx=PADX, pady=PADY*2)

    def cleaning_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def waiter_menu(self):
        # Waiter Window Setup
        waiter_window = tk.Toplevel(self.window)
        waiter_window.title("Crazy Pizza Order Services")

        self.left = int(self.display_width / 2 - (WINDOW_WIDTH / 2))
        self.top = int(self.display_height / 2 - (WINDOW_HEIGHT / 2))
        waiter_window.geometry(f"{int(WINDOW_WIDTH*1.5)}x{int(WINDOW_HEIGHT*1.2)}+{self.left}+{self.top}")
        waiter_window.config(padx=PADX, pady=PADY)
        waiter_window.minsize(int(WINDOW_WIDTH*1.5 / 1.25), int(WINDOW_HEIGHT*1.2 / 1.25))

        # Multiple tabs for the waiter window
        notebook = ttk.Notebook(waiter_window)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        notebook.add(tab1, text="Take Orders")
        notebook.add(tab2, text="Active Orders")
        notebook.add(tab3, text="Finished Orders")
        notebook.pack(fill=tk.BOTH)

        # First tab frames
        left_frame1 = ttk.Frame(tab1, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame1.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame1 = ttk.Frame(tab1, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame1.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame1.pack_propagate(False)

        self.display_waiter_logo(left_frame1)

        # Second tab frames
        left_frame2 = ttk.Frame(tab2, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame2.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame2 = ttk.Frame(tab2, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame2.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame2.pack_propagate(False)

        self.display_waiter_logo(left_frame2)

        left_frame3 = ttk.Frame(tab3, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame3.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame3 = ttk.Frame(tab3, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame3.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame3.pack_propagate(False)

        self.display_waiter_logo(left_frame3)

        # product instances
        self.pizza = Pizza()
        self.snack = Snack()
        self.drink = Drink()

        pizzas_button = ttk.Button(left_frame1, text="Pizzas", command=lambda: show_menu(right_frame1, "pizzas"))
        pizzas_button.grid(row=1, column=0, padx=PADX, pady=PADY)
        snacks_button = ttk.Button(left_frame1, text="Snacks", command=lambda: show_menu(right_frame1, "snacks"))
        snacks_button.grid(row=1, column=1, padx=PADX, pady=PADY)
        drinks_button = ttk.Button(left_frame1, text="Drinks", command=lambda: show_menu(right_frame1, "drinks"))
        drinks_button.grid(row=1, column=2, padx=PADX, pady=PADY)

        # Order related functions
        @handle_errors
        def show_active_orders(frame):
            global tree_active_orders
            self.cleaning_frame(frame)
            tree_active_orders = ttk.Treeview(frame, show="headings", selectmode="browse")
            tree_active_orders["columns"] = (
                "Order ID", "Table No", "Total Price", "Order Date", "Order Hour", "Items")
            tree_active_orders.column("Order ID", anchor="center", width=80)
            tree_active_orders.column("Table No", anchor="center", width=100)
            tree_active_orders.column("Total Price", anchor="center", width=100)
            tree_active_orders.column("Order Date", anchor="center", width=100)
            tree_active_orders.column("Order Hour", anchor="center", width=100)
            tree_active_orders.column("Items", anchor="center", width=300)
            tree_active_orders.heading("Order ID", text="Order ID")
            tree_active_orders.heading("Table No", text="Table No")
            tree_active_orders.heading("Total Price", text="Total Price")
            tree_active_orders.heading("Order Date", text="Order Date")
            tree_active_orders.heading("Order Hour", text="Order Hour")
            tree_active_orders.heading("Items", text="Items")
            tree_active_orders.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            active_orders = self.active_orders.get_active_orders()
            print(f"Active Orders: {active_orders}")
            for order in active_orders:
                table_no = self.customers.get_table_no(order[1])
                print(f"Inserting order: {order}")
                order_with_table = (order[0], table_no, order[2], order[3], order[4], order[5])
                tree_active_orders.insert("", "end", values=order_with_table)

        @handle_errors
        def show_finished_orders(frame):
            self.cleaning_frame(frame)
            tree_finished_orders = ttk.Treeview(frame, show="headings", selectmode="browse")
            tree_finished_orders["columns"] = (
                "Order ID", "Table No", "Total Price", "Order Date", "Order Hour", "Prepared Hour", "Items")
            tree_finished_orders.column("Order ID", anchor="center", width=80)
            tree_finished_orders.column("Table No", anchor="center", width=100)
            tree_finished_orders.column("Total Price", anchor="center", width=100)
            tree_finished_orders.column("Order Date", anchor="center", width=100)
            tree_finished_orders.column("Order Hour", anchor="center", width=100)
            tree_finished_orders.column("Prepared Hour", anchor="center", width=100)
            tree_finished_orders.column("Items", anchor="center", width=300)
            tree_finished_orders.heading("Order ID", text="Order ID")
            tree_finished_orders.heading("Table No", text="Table No")
            tree_finished_orders.heading("Total Price", text="Total Price")
            tree_finished_orders.heading("Order Date", text="Order Date")
            tree_finished_orders.heading("Order Hour", text="Order Hour")
            tree_finished_orders.heading("Prepared Hour", text="Prepared Hour")
            tree_finished_orders.heading("Items", text="Items")
            tree_finished_orders.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            finished_orders = self.finished_orders.get_finished_orders()
            for order in finished_orders:
                table_no = self.customers.get_table_no(order[1])
                print(f"Inserting order: {order}")
                order_with_table = (order[0], table_no, order[2], order[3], order[4], order[5], order[6])
                tree_finished_orders.insert("", "end", values=order_with_table)

        @handle_errors
        def cancel_order(frame):
            selected_item = tree_active_orders.selection()
            if selected_item:
                order_id = tree_active_orders.item(selected_item, 'values')[0]
                self.active_orders.cancel_order(order_id)
                show_active_orders(frame)
            else:
                messagebox.showwarning("Selection Error", "Please select an order to cancel.")

        @handle_errors
        def update_item_list(event):
            selected_item_type = item_type_combobox.get()
            if selected_item_type == "Pizza":
                items = self.pizza.list_products()
            elif selected_item_type == "Snack":
                items = self.snack.list_products()
            elif selected_item_type == "Drink":
                items = self.drink.list_products()
            item_combobox['values'] = [item[2] for item in items]

        @handle_errors
        def show_product_details(event):
            selected_item_name = item_combobox.get()
            print(selected_item_name)
            selected_item_type = item_type_combobox.get()
            if selected_item_type == "Pizza":
                product_attributes = self.pizza.select_product(selected_item_name)
            elif selected_item_type == "Snack":
                product_attributes = self.snack.select_product(selected_item_name)
            elif selected_item_type == "Drink":
                product_attributes = self.drink.select_product(selected_item_name)
            item_id_label['text'] = product_attributes[0]
            item_name_label['text'] = product_attributes[2]
            item_price_label['text'] = product_attributes[3]

        @handle_errors
        def get_order_details():
            selected_item_name = item_combobox.get()
            print(selected_item_name)
            selected_item_type = item_type_combobox.get()
            if selected_item_type == "Pizza":
                product_attributes = self.pizza.select_product(selected_item_name)
            elif selected_item_type == "Snack":
                product_attributes = self.snack.select_product(selected_item_name)
            elif selected_item_type == "Drink":
                product_attributes = self.drink.select_product(selected_item_name)
            item_id = product_attributes[0]
            item_type = product_attributes[1]
            item_name = product_attributes[2]
            item_price = product_attributes[3]
            item_quantity = spinbox_int.get()
            if item_quantity != 0:
                item_details = (item_id, item_type, item_name, item_price, item_quantity)
                return item_details
            else:
                messagebox.showwarning(title="Error!", message="Quantity must be greater than '0'")

        # Adding selected item to the current order
        @handle_errors
        def add_to_order():
            global total_price
            item_details = get_order_details()
            if item_details:
                quantity = item_details[4]
                total_price += item_details[3] * quantity
                total_price_amount_label.config(text=str(total_price))
                current_item_name = item_details[2]
                total_orders_text = total_orders_name_label.cget("text")
                total_orders_text += ", " + str(quantity) + " " + current_item_name
                total_orders_name_label.config(text=total_orders_text)

                self.items.append(item_details)
            else:
                total_price_amount_label.config(text="")

        @handle_errors
        def refresh_labels():
            total_price_amount_label.config(text="")
            total_orders_name_label.config(text="")
            self.items = []
            update_item_list(None)

        # New window for submitting an order
        @handle_errors
        def completing_order():
            def show_temp_customer_frame():
                temp_customer_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                perm_customer_frame.grid_forget()

            def show_perm_customer_frame():
                perm_customer_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                temp_customer_frame.grid_forget()

            def submit_order():
                customer_type = customer_type_var.get()
                customer_id = None
                total_float_price = (total_price_amount_label.cget('text'))
                if customer_type == 0:
                    table_no = table_no_entry.get()
                    first_name = temp_first_name_entry.get()
                    last_name = temp_last_name_entry.get()
                    if table_no and first_name and last_name:
                        customer_id = self.customers.add_temp_customer(table_no, first_name, last_name)
                elif customer_type == 1:
                    first_name = perm_first_name_entry.get()
                    last_name = perm_last_name_entry.get()
                    email = email_entry.get()
                    address = address_entry.get()
                    if first_name and last_name and email and address:
                        customer_id = self.customers.add_perm_customer(first_name, last_name, email, address)

                if customer_id:
                    self.active_orders.take_order(customer_type, customer_id, self.items, total_float_price)
                    messagebox.showinfo("Order Completed", "The order has been successfully completed!")
                    refresh_labels()
                    order_window.destroy()
                else:
                    messagebox.showerror("Oops!", "Please fill in all the required fields.")

            order_window = tk.Toplevel(self.window)
            order_window.title("Complete Order")
            order_window.geometry("350x300")
            order_window.resizable(False, False)

            customer_type_var = tk.IntVar(value=0)
            temp_customer_rb = ttk.Radiobutton(order_window, text="Temporary Customer", variable=customer_type_var,
                                               value=0, command=show_temp_customer_frame)
            perm_customer_rb = ttk.Radiobutton(order_window, text="Permanent Customer", variable=customer_type_var,
                                               value=1, command=show_perm_customer_frame)
            temp_customer_rb.grid(row=0, column=0, padx=10, pady=10)
            perm_customer_rb.grid(row=0, column=1, padx=10, pady=10)

            temp_customer_frame = ttk.Frame(order_window)
            table_no_label = ttk.Label(temp_customer_frame, text="Table No:")
            table_no_label.grid(row=0, column=0, padx=10, pady=10)
            table_no_entry = ttk.Entry(temp_customer_frame)
            table_no_entry.grid(row=0, column=1, padx=10, pady=10)

            temp_first_name_label = ttk.Label(temp_customer_frame, text="First Name:")
            temp_first_name_label.grid(row=1, column=0, padx=10, pady=10)
            temp_first_name_entry = ttk.Entry(temp_customer_frame)
            temp_first_name_entry.grid(row=1, column=1, padx=10, pady=10)

            temp_last_name_label = ttk.Label(temp_customer_frame, text="Last Name:")
            temp_last_name_label.grid(row=2, column=0, padx=10, pady=10)
            temp_last_name_entry = ttk.Entry(temp_customer_frame)
            temp_last_name_entry.grid(row=2, column=1, padx=10, pady=10)

            perm_customer_frame = ttk.Frame(order_window)
            perm_first_name_label = ttk.Label(perm_customer_frame, text="First Name:")
            perm_first_name_label.grid(row=0, column=0, padx=10, pady=10)
            perm_first_name_entry = ttk.Entry(perm_customer_frame)
            perm_first_name_entry.grid(row=0, column=1, padx=10, pady=10)

            perm_last_name_label = ttk.Label(perm_customer_frame, text="Last Name:")
            perm_last_name_label.grid(row=1, column=0, padx=10, pady=10)
            perm_last_name_entry = ttk.Entry(perm_customer_frame)
            perm_last_name_entry.grid(row=1, column=1, padx=10, pady=10)

            email_label = ttk.Label(perm_customer_frame, text="Email:")
            email_label.grid(row=2, column=0, padx=10, pady=10)
            email_entry = ttk.Entry(perm_customer_frame)
            email_entry.grid(row=2, column=1, padx=10, pady=10)

            address_label = ttk.Label(perm_customer_frame, text="Address:")
            address_label.grid(row=3, column=0, padx=10, pady=10)
            address_entry = ttk.Entry(perm_customer_frame)
            address_entry.grid(row=3, column=1, padx=10, pady=10)

            submit_button = ttk.Button(order_window, text="Submit Order", command=submit_order)
            submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            show_temp_customer_frame()

        item_type_combobox_label = ttk.Label(left_frame1, text="Product Type")
        item_type_combobox_label.grid(row=2, column=0)
        item_combobox_label = ttk.Label(left_frame1, text="Product Name")
        item_combobox_label.grid(row=2, column=1)
        item_quantity_spinbox_label = ttk.Label(left_frame1, text="Quantity")
        item_quantity_spinbox_label.grid(row=2, column=2)

        # Item type combobox
        item_type_combobox = ttk.Combobox(left_frame1, values=["Pizza", "Snack", "Drink"], width=10)
        item_type_combobox.grid(row=3, column=0)
        item_type_combobox.bind("<<ComboboxSelected>>", update_item_list)

        # Item list combobox
        item_combobox = ttk.Combobox(left_frame1, width=10)
        item_combobox.grid(row=3, column=1)
        item_combobox.bind("<<ComboboxSelected>>", show_product_details)

        # Item quantity spinbox
        spinbox_int = tk.IntVar(value=0)
        item_quantity_spinbox = ttk.Spinbox(left_frame1, from_=1, to=20, width=10,
                                            command=lambda: print(spinbox_int.get()), textvariable=spinbox_int)
        item_quantity_spinbox.grid(row=3, column=2)

        product_id = ttk.Label(left_frame1, text="Product ID:")
        product_id.grid(row=4, column=0, padx=PADX, pady=PADY*2)
        item_id_label = ttk.Label(left_frame1, text="")
        item_id_label.grid(row=4, column=1, padx=PADX, pady=PADY*2)
        product_name = ttk.Label(left_frame1, text="Product Name:")
        product_name.grid(row=5, column=0, padx=PADX, pady=PADY*2)
        item_name_label = ttk.Label(left_frame1, text="")
        item_name_label.grid(row=5, column=1, padx=PADX, pady=PADY*2)
        product_price = ttk.Label(left_frame1, text="Product Price:")
        product_price.grid(row=6, column=0, padx=PADX, pady=PADY)
        item_price_label = ttk.Label(left_frame1, text="")
        item_price_label.grid(row=6, column=1, padx=PADX, pady=PADY)
        product_quantity = ttk.Label(left_frame1, text="Quantity:")
        product_quantity.grid(row=7, column=0, padx=PADX, pady=PADY*2)
        item_quantity_label = ttk.Label(left_frame1, textvariable=spinbox_int)
        item_quantity_label.grid(row=7, column=1, padx=PADX, pady=PADY*2)

        total_price_label = ttk.Label(left_frame1, text="Total: ")
        total_price_label.grid(row=9, column=0, padx=PADX, pady=PADY)
        total_price_amount_label = ttk.Label(left_frame1, text="")
        total_price_amount_label.grid(row=9, column=1, padx=PADX, pady=PADY)
        total_orders_label = ttk.Label(left_frame1, text="Ordered items: ")
        total_orders_label.grid(row=10, column=0, padx=PADX, pady=PADY)
        total_orders_name_label = ttk.Label(left_frame1, text="")
        total_orders_name_label.grid(row=10, column=1, columnspan=3, padx=PADX)

        add_to_order_button = ttk.Button(left_frame1, text="Add to Order", command=add_to_order)
        add_to_order_button.grid(row=8, column=1, padx=PADX, pady=PADY)
        complete_order = ttk.Button(left_frame1, text="Complete Order", command=completing_order)
        complete_order.grid(row=11, column=1, padx=PADX, pady=PADY)

        # Placing grip at the corner
        grip = ttk.Sizegrip(waiter_window)
        grip.place(relx=1.0, rely=1.0, anchor="se")

        @handle_errors
        def show_menu(frame, item_type):
            self.cleaning_frame(frame)
            self.tree_menu = ttk.Treeview(frame, show="headings", selectmode="browse")
            self.tree_menu["columns"] = ("ID", "Type", "Name", "Price", "Ingredients")
            self.tree_menu.column("ID", anchor="center", width=25)
            self.tree_menu.column("Type", anchor="center", width=50)
            self.tree_menu.column("Name", anchor="center", width=200)
            self.tree_menu.column("Price", anchor="center", width=50)
            self.tree_menu.column("Ingredients", anchor="center", width=400)
            self.tree_menu.heading("ID", text="ID")
            self.tree_menu.heading("Type", text="Type")
            self.tree_menu.heading("Name", text="Name")
            self.tree_menu.heading("Price", text="Price")
            self.tree_menu.heading("Ingredients", text="Ingredients")
            self.tree_menu.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            self.pizza = Pizza()
            self.snack = Snack()
            self.drink = Drink()

            pizzas = self.pizza.list_products()
            snacks = self.snack.list_products()
            drinks = self.drink.list_products()

            if item_type == "pizzas":
                for pizza in pizzas:
                    self.tree_menu.insert("", "end", values=(pizza[0], "Pizza", pizza[2], pizza[3], pizza[4]))
            elif item_type == "snacks":
                for snack in snacks:
                    self.tree_menu.insert("", "end", values=(snack[0], "Snack", snack[2], snack[3], snack[4]))
            else:
                for drink in drinks:
                    self.tree_menu.insert("", "end", values=(drink[0], "Drink", drink[2], drink[3], drink[4]))

        # Second tab buttons
        active_orders_button = ttk.Button(left_frame2, text="Show Active Orders",
                                          command=lambda: show_active_orders(right_frame2))
        active_orders_button.grid(row=1, column=1, padx=PADX, pady=PADY)
        cancel_order_button = ttk.Button(left_frame2, text="Cancel Order", command=lambda: cancel_order(right_frame2))
        cancel_order_button.grid(row=2, column=1, padx=PADX, pady=PADY)

        # Third tab buttons
        finished_orders_button = ttk.Button(left_frame3, text="Show Finished Orders",
                                            command=lambda: show_finished_orders(right_frame3))
        finished_orders_button.grid(row=1, column=1, padx=PADX, pady=PADY*3)

        notebook.bind("<<NotebookTabChanged>>",
                      lambda event: show_active_orders(right_frame2) if notebook.index("current") == 1 else None)
        notebook.bind("<<NotebookTabChanged>>",
                      lambda event: show_finished_orders(right_frame3) if notebook.index("current") == 2 else None)

    def chef_menu(self):
        # Chef Window Setup
        chef_window = tk.Toplevel(self.window)
        chef_window.title("Crazy Pizza Cooking Services")

        self.left = int(self.display_width / 2 - (WINDOW_WIDTH / 2))
        self.top = int(self.display_height / 2 - (WINDOW_HEIGHT / 2))
        chef_window.geometry(f"{int(WINDOW_WIDTH*1.5)}x{int(WINDOW_HEIGHT*1.2)}+{self.left}+{self.top}")
        chef_window.config(padx=PADX, pady=PADY)
        chef_window.minsize(int(WINDOW_WIDTH*1.5 / 1.25), int(WINDOW_HEIGHT*1.2 / 1.25))

        # Multiple tabs for the chef window
        notebook = ttk.Notebook(chef_window)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        notebook.add(tab1, text="Restaurant Menu")
        notebook.add(tab2, text="Active Orders")
        notebook.add(tab3, text="Finished Orders")
        notebook.pack(fill=tk.BOTH)

        # First tab frames
        left_frame1 = ttk.Frame(tab1, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame1.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame1 = ttk.Frame(tab1, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame1.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame1.pack_propagate(False)

        self.display_chef_logo(left_frame1)

        # Second tab frames
        left_frame2 = ttk.Frame(tab2, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame2.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame2 = ttk.Frame(tab2, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame2.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame2.pack_propagate(False)

        self.display_chef_logo(left_frame2)

        # Third tab frames
        left_frame3 = ttk.Frame(tab3, width=280, height=self.display_height, relief=tk.GROOVE)
        left_frame3.pack(side="left", fill=tk.Y, expand=True, padx=PADX)
        right_frame3 = ttk.Frame(tab3, width=self.display_width, height=self.display_height, relief=tk.GROOVE)
        right_frame3.pack(side="left", fill=tk.BOTH, expand=True)
        right_frame3.pack_propagate(False)

        self.display_chef_logo(left_frame3)

        # First Tab buttons
        pizzas_button = ttk.Button(left_frame1, text="Pizzas", command=lambda: show_menu(right_frame1, "pizzas"))
        pizzas_button.grid(row=1, column=1, padx=PADX, pady=PADY)
        snacks_button = ttk.Button(left_frame1, text="Snacks", command=lambda: show_menu(right_frame1, "snacks"))
        snacks_button.grid(row=2, column=1, padx=PADX, pady=PADY)
        drinks_button = ttk.Button(left_frame1, text="Drinks", command=lambda: show_menu(right_frame1, "drinks"))
        drinks_button.grid(row=3, column=1, padx=PADX, pady=PADY)

        # Order related Buttons
        @handle_errors
        def order_ready(frame):
            global tree_active_orders
            selected_item = tree_active_orders.selection()
            if selected_item:
                order_id = tree_active_orders.item(selected_item, 'values')[0]
                self.active_orders.finished_order(order_id)
                show_active_orders(frame)
            else:
                messagebox.showwarning("Selection Error", "Please select the prepared order.")

        @handle_errors
        def show_active_orders(frame):
            global tree_active_orders
            self.cleaning_frame(frame)
            tree_active_orders = ttk.Treeview(frame, show="headings", selectmode="browse")
            tree_active_orders["columns"] = (
                "Order ID", "Table No", "Total Price", "Order Date", "Order Hour", "Items")
            tree_active_orders.column("Order ID", anchor="center", width=80)
            tree_active_orders.column("Table No", anchor="center", width=100)
            tree_active_orders.column("Total Price", anchor="center", width=100)
            tree_active_orders.column("Order Date", anchor="center", width=100)
            tree_active_orders.column("Order Hour", anchor="center", width=100)
            tree_active_orders.column("Items", anchor="center", width=300)
            tree_active_orders.heading("Order ID", text="Order ID")
            tree_active_orders.heading("Table No", text="Table No")
            tree_active_orders.heading("Total Price", text="Total Price")
            tree_active_orders.heading("Order Date", text="Order Date")
            tree_active_orders.heading("Order Hour", text="Order Hour")
            tree_active_orders.heading("Items", text="Items")
            tree_active_orders.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            active_orders = self.active_orders.get_active_orders()
            print(f"Active Orders: {active_orders}")
            for order in active_orders:
                table_no = self.customers.get_table_no(order[1])
                print(f"Inserting order: {order}")
                order_with_table = (order[0], table_no, order[2], order[3], order[4], order[5])
                tree_active_orders.insert("", "end", values=order_with_table)

        @handle_errors
        def show_finished_orders(frame):
            self.cleaning_frame(frame)
            tree_finished_orders = ttk.Treeview(frame, show="headings", selectmode="browse")
            tree_finished_orders["columns"] = (
                "Order ID", "Table No", "Total Price", "Order Date", "Order Hour", "Prepared Hour", "Items")
            tree_finished_orders.column("Order ID", anchor="center", width=80)
            tree_finished_orders.column("Table No", anchor="center", width=100)
            tree_finished_orders.column("Total Price", anchor="center", width=100)
            tree_finished_orders.column("Order Date", anchor="center", width=100)
            tree_finished_orders.column("Order Hour", anchor="center", width=100)
            tree_finished_orders.column("Prepared Hour", anchor="center", width=100)
            tree_finished_orders.column("Items", anchor="center", width=300)
            tree_finished_orders.heading("Order ID", text="Order ID")
            tree_finished_orders.heading("Table No", text="Table No")
            tree_finished_orders.heading("Total Price", text="Total Price")
            tree_finished_orders.heading("Order Date", text="Order Date")
            tree_finished_orders.heading("Order Hour", text="Order Hour")
            tree_finished_orders.heading("Prepared Hour", text="Prepared Hour")
            tree_finished_orders.heading("Items", text="Items")
            tree_finished_orders.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            finished_orders = self.finished_orders.get_finished_orders()
            for order in finished_orders:
                table_no = self.customers.get_table_no(order[1])
                print(f"Inserting order: {order}")
                order_with_table = (order[0], table_no, order[2], order[3], order[4], order[5], order[6])
                tree_finished_orders.insert("", "end", values=order_with_table)

        # Placing grip at the corner
        grip = ttk.Sizegrip(chef_window)
        grip.place(relx=1.0, rely=1.0, anchor="se")

        @handle_errors
        def show_menu(frame, item_type):
            self.cleaning_frame(frame)
            self.tree_menu = ttk.Treeview(frame, show="headings", selectmode="browse")
            self.tree_menu["columns"] = ("ID", "Type", "Name", "Price", "Ingredients")
            self.tree_menu.column("ID", anchor="center", width=25)
            self.tree_menu.column("Type", anchor="center", width=50)
            self.tree_menu.column("Name", anchor="center", width=200)
            self.tree_menu.column("Price", anchor="center", width=50)
            self.tree_menu.column("Ingredients", anchor="center", width=400)
            self.tree_menu.heading("ID", text="ID")
            self.tree_menu.heading("Type", text="Type")
            self.tree_menu.heading("Name", text="Name")
            self.tree_menu.heading("Price", text="Price")
            self.tree_menu.heading("Ingredients", text="Ingredients")
            self.tree_menu.pack(padx=PADX, pady=PADY, expand=True, fill=tk.BOTH)

            self.pizza = Pizza()
            self.snack = Snack()
            self.drink = Drink()

            pizzas = self.pizza.list_products()
            snacks = self.snack.list_products()
            drinks = self.drink.list_products()

            if item_type == "pizzas":
                for pizza in pizzas:
                    self.tree_menu.insert("", "end", values=(pizza[0], "Pizza", pizza[2], pizza[3], pizza[4]))
            elif item_type == "snacks":
                for snack in snacks:
                    self.tree_menu.insert("", "end", values=(snack[0], "Snack", snack[2], snack[3], snack[4]))
            else:
                for drink in drinks:
                    self.tree_menu.insert("", "end", values=(drink[0], "Drink", drink[2], drink[3], drink[4]))

        # Second tab buttons
        active_orders_button = ttk.Button(left_frame2, text="Show Active Orders",
                                          command=lambda: show_active_orders(right_frame2))
        active_orders_button.grid(row=1, column=1, padx=PADX, pady=PADY)
        order_ready_button = ttk.Button(left_frame2, text="Order Ready", command=lambda: order_ready(right_frame2))
        order_ready_button.grid(row=2, column=1, padx=PADX, pady=PADY)

        # Third tab buttons
        finished_orders_button = ttk.Button(left_frame3, text="Show Finished Orders",
                                            command=lambda: show_finished_orders(right_frame3))
        finished_orders_button.grid(row=1, column=1, padx=PADX, pady=PADY*3)

        notebook.bind("<<NotebookTabChanged>>",
                      lambda event: show_active_orders(right_frame2) if notebook.index("current") == 1 else None)
        notebook.bind("<<NotebookTabChanged>>",
                      lambda event: show_finished_orders(right_frame3) if notebook.index("current") == 2 else None)

    # Logo related functions
    def display_manager_logo(self, frame):
        logo_canvas = tk.Canvas(frame, width=374, height=275)
        logo_canvas.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY * 2)
        manager_image = tk.PhotoImage(file="crazy_manager_logo.png")
        logo_canvas.create_image(187, 138, image=manager_image)
        self.manager_images.append(manager_image)

    def display_waiter_logo(self, frame):
        logo_canvas = tk.Canvas(frame, width=374, height=275)
        logo_canvas.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY * 2)
        waiter_image = tk.PhotoImage(file="crazy_waiter_logo.png")
        logo_canvas.create_image(187, 138, image=waiter_image)
        self.waiter_images.append(waiter_image)

    def display_chef_logo(self, frame):
        logo_canvas = tk.Canvas(frame, width=374, height=275)
        logo_canvas.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY * 2)
        chef_image = tk.PhotoImage(file="crazy_chef_logo.png")
        logo_canvas.create_image(187, 138, image=chef_image)
        self.chef_images.append(chef_image)


def main():
    window = tk.Tk()
    app = GUI(window)
    app.window.mainloop()


if __name__ == "__main__":
    main()


