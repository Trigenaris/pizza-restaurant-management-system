<!-- Main Headline Here... -->
<h1 align='center'> 🍕 Pizza Restaurant Management System (In Progress) </h1>

<div align="center">
    <img src="https://github.com/Trigenaris/pizza-restaurant-management-system/blob/main/crazy_logo.png">
</div>

In this project; we focus on a **Restaurant Management**, specifically a made-up restaurant called *Crazy Pizza Restaurant*. The restaurant management system has a menu stored in a database that contains *CRUD* operations and has a system in which any item can be ordered. Also, orders are part of the database structure to analyze the current situation of the restaurant. The main features of the system are as shown with the help of the referred modules and libraries:

## 📌 Required Modules:
* sqlite3
* tkinter
* datetime
* pandas
* matplotlib
* functools (for the decorator)
* winsound (for the custom message boxes)

#### ❓ Abbreviations: 
* **EF:** Some of the features that are signed as **EF** means **extra features** which can be excluded in the final version of the project.
* **WIP:** Headlines signed as **WIP** means **work in progress** which are not fully completed yet.

<hr>

## 📌 Main Features:
* **login system** for the user to see the related menu on their screen.
* 3 main menus refer to roles respectively: **Manager, Waiter, Chef**
* It is planned that the system will have **custom message boxes** other than default ones in the tkinter. (WIP) (EF)
* Different roles have **different functionalities** to do that are **responsive** to each other.

### 👩‍💼 Features of the Manager:
* Editing the menu (**Adding, updating or removing products**)
* Checking the current, canceled, or completed orders.
* Checking, and analyzing daily, weekly, monthly, or yearly reports.

### 🤵‍♀️ Features of the Waiter: 
* Checking the Menu.
* Taking orders.
* Cancelling orders.
* Pinging **the taken orders** to the chef.

### 👩‍🍳 Features of the Chef:
* Checking the Menu.
* Checking the taken orders.
* Pinging **the prepared orders** to the waiter.

<hr>

The project will have notices as it progresses in the future.

<hr>

<h2>
    How Does It Work?
</h2>

The application starts with a login screen that expects the user to log in from one of the three roles:

* 1️⃣ First the user chooses the role
* 2️⃣ Then enters the password (Only for the manager)
* 3️⃣ Lastly, clicks the login button

![pizza1](https://github.com/Trigenaris/pizza-restaurant-management-system/assets/122381599/a102a1ec-e0a3-4403-bc36-7da03b6d0972)

# Manager Menu

After logging in, the related menu appears on the screen. (Manager menu for example)

## Show Menu

* There are four different tabs for different functionalities in the manager menu.
* 1️⃣ As the user clicks `Show Menu` button, 2️⃣ whole products appear on the right frame.

![pizza2](https://github.com/Trigenaris/pizza-restaurant-management-system/assets/122381599/2cab8763-fd0c-4f45-b803-0b8bab81bd5c)

## New Product

* 1️⃣ The user clicks the `New Product` button,
* 2️⃣ A new window appears to be filled in,
* 3️⃣ The user clicks the `Add Product` button to add the product to the menu and the database:

![pizza3](https://github.com/Trigenaris/pizza-restaurant-management-system/assets/122381599/acc82845-ee91-4a67-b339-b83f3b981c0f)
![pizza4](https://github.com/Trigenaris/pizza-restaurant-management-system/assets/122381599/e6125be6-74e8-4c82-acdd-d04866f4015b)
![pizza5](https://github.com/Trigenaris/pizza-restaurant-management-system/assets/122381599/f63bbd66-1a57-419c-9a5d-31cd49e00404)




