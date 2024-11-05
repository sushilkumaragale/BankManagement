Bank Management System (Python)

Overview
This Bank Management System is a Python-based application that allows admins and users to perform basic banking operations, such as creating accounts, making deposits and withdrawals, checking balances, and viewing transaction histories. The system uses MySQL for data storage and management, ensuring that all user and admin data is securely handled.

Features:
Admin Login: Admins can log in and manage user accounts, including creating new users or admins, updating user details, and deleting user accounts.
User Login: Users can log in to view and manage their personal account, make deposits, withdrawals, check balance, and view their transaction history.
Database Integration: The system uses MySQL to store user and admin data, transaction history, and account balances.
Technologies Used:
Python 3.x
MySQL (for database management)
PrettyTable (for displaying data in tabular form)
Installation Instructions
Prerequisites:
Python 3.x
MySQL (installed and running)
MySQL Connector for Python (mysql-connector-python)
PrettyTable (for displaying tabular data)
Step 1: Clone the repository
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/bank-management-system.git
cd bank-management-system
Step 2: Install required Python dependencies
You can install the required dependencies using pip:

bash
Copy code
pip install mysql-connector-python prettytable
Step 3: Set up the MySQL database
Install MySQL and start the MySQL server.
Log in to MySQL and create a new database (e.g., finale1):
sql
Copy code
CREATE DATABASE finale1;
Import the provided SQL schema into your MySQL database. If not provided, the system will create tables automatically when you run the script.
Step 4: Update database connection settings
In the main.py file, ensure that the MySQL connection parameters are set correctly:

python
Copy code
conn = mysql.connector.connect(host='localhost', password='YourPassword', user='root', database='finale1')
Make sure to replace 'YourPassword' with your MySQL root password.

Step 5: Run the Application
Run the Python script to start the Bank Management System:

bash
Copy code
python main.py
Features Overview
Admin Panel:
Login: Admins can log in with their unique admin_id and password.
Create User Account: Admins can create new user accounts by entering personal information and balance.
Create Admin Account: Admins can create other admin accounts with unique admin_id and password.
Update User Account: Admins can update user account details (e.g., name, balance).
Delete User Account: Admins can delete a user account from the system.
View User List: Admins can view a list of all users with account details.
User Panel:
Login: Users can log in using their account_no and password.
Deposit: Users can deposit money into their account.
Withdraw: Users can withdraw money from their account.
Check Balance: Users can check their current balance.
Transaction History: Users can view a history of all transactions (deposits and withdrawals).
Code Structure
main.py: The main script that handles the logic for both user and admin interactions.
PrettyTable: Used for displaying data in tabular format (e.g., user details, transaction history).
MySQL Queries: SQL queries are embedded in the Python code to manage the database (creating tables, inserting, updating, and deleting records).
Example Usage:
Admin Operations:
Admin logs in with their admin_id and password.
Admin can create new user accounts or new admin accounts, view existing users, or delete users.
User Operations:
User logs in with their account_no and password.
User can deposit, withdraw, check balance, or view transaction history.
Sample Admin Workflow:
bash
Copy code
Admin Login
1. Create a User Account
2. Create an Admin Account
3. Update User Details
4. Delete User Details
5. Show User Details
6. Exit
Sample User Workflow:
bash
Copy code
User Login
1. Withdraw
2. Deposit
3. Check Balance
4. Transaction History
5. Exit
