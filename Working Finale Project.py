import mysql.connector
from prettytable import PrettyTable
import random
from decimal import Decimal

conn = mysql.connector.connect(host='localhost', password='Mysql@123', user='root', database='finale1')
cursor = conn.cursor()

create_user_table_query = """
CREATE TABLE IF NOT EXISTS user_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    account_no INT UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    user_pas VARCHAR(255),
    balance DECIMAL(10, 2)
)
"""
cursor.execute(create_user_table_query)

create_admin_table_query = """
CREATE TABLE IF NOT EXISTS admin_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    admin_pas VARCHAR(255)
)
"""
cursor.execute(create_admin_table_query)

create_transaction_history_table_query = """
CREATE TABLE IF NOT EXISTS transaction_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    remarks VARCHAR(255),
    amount DECIMAL(10, 2),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
cursor.execute(create_transaction_history_table_query)

def generate_unique_id():
    return random.randint(0, 99)

def generate_unique_account_no():
    return random.randint(10000, 999999999)

def admin():
    print("*" * 10,"ADMIN LOGIN PANNEL","*" * 10)
    
    admin_id = int(input("Enter an admin ID: "))
    admin_pas = input("Enter a Password:")
    
    cursor.execute("SELECT * FROM admin_accounts WHERE admin_id = %s AND admin_pas = %s", (admin_id, admin_pas))
    admin = cursor.fetchone()

    if admin:
        print("Admin login successful")
        return admin
    else:
        print("Invalid admin ID or password")
        return None

def user():
    print("*" * 10,"USER LOGIN PANNEL","*" * 10)
    account_no = int(input("Enter an account number: "))
    user_pas = input("Enter a Password: ")

    cursor.execute("SELECT * FROM user_accounts WHERE account_no = %s AND user_pas = %s", (account_no, user_pas))
    user = cursor.fetchone()

    if user:
        print("User login Successful")
        return user
    else:
        print("Invalid account number or password")
        return None

def create_admin_ac(admin):
    print("*" * 10,"CREATE ADMIN ACCOUNT","*" * 10)
    fname = input("Enter First Name: ")
    lname = input("Enter Last Name: ")
    admin_pas = input("Create Password:")

    admin_id = generate_unique_id()

    insert_query = """
    INSERT INTO admin_accounts (admin_id, first_name, last_name, admin_pas)
    VALUES (%s, %s, %s, %s)
    """
    data = (admin_id, fname, lname, admin_pas)
    cursor.execute(insert_query, data)

    conn.commit()

    print(f"Admin Account Created with Admin ID: {admin_id}")

def create_user_ac(admin):
    print("*" * 10,"CREATE USER ACCOUNT","*" * 10)
    fname = input("Enter First Name: ")
    lname = input("Enter Last Name: ")
    user_pas = input("Create Password:")

    user_id = generate_unique_id()
    account_no = generate_unique_account_no()

    balance = float(input("Enter balance: "))

    insert_query = """
    INSERT INTO user_accounts (user_id, account_no, first_name, last_name, user_pas, balance)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (user_id, account_no, fname, lname, user_pas, balance)
    cursor.execute(insert_query, data)

    conn.commit()

    print(f"User Account Created with User ID: {user_id} and Account No: {account_no}")

def update_user_detail(admin):
    print("*" * 10,"UPDATE USER DETAILS","*" * 10)
    user_id = int(input("Enter the User ID to update: "))
    
    cursor.execute("SELECT user_id, account_no, first_name, last_name, balance FROM user_accounts WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        table = PrettyTable()
        table.field_names = ["User ID", "Account No", "First Name", "Last Name", "Balance"]
        table.add_row(user)  
        print(table)
    else:
        print("User not found.")
        return  

    conf = input("Are you sure you want to update your account details?\n(y/n)\n")
    if conf.lower() == "y":
        newfname = input("Enter your new First Name: ")
        newlname = input("Enter your New Last Name: ")
        new_balance = float(input("Enter the new balance: "))
        newpas = input("Enter the new password: ")
        confnewpass = input("Confirm password: ")
        while True:
            if newpas == confnewpass:
                print("Password changed successfully")
                break
            else:
                print("Password Not Same")

        # Fixed the INSERT query and removed the extra comma
        insert_query = """
        UPDATE user_accounts
        SET first_name=%s, last_name=%s, balance=%s, user_pas=%s
        WHERE user_id=%s
        """
        data = (newfname, newlname, new_balance, confnewpass, user_id)
        cursor.execute(insert_query, data)
        print("User details updated")
        conn.commit()
    else:
        print("Account update canceled.")
    conn.commit()

def delete_user_details(admin):
    print("*" * 10,"DELETE USER DETAILS","*" * 10)
    user_id = int(input("Enter the User ID to delete: "))

    cursor.execute("SELECT * FROM user_accounts WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if user is None:
        print("User not found.")
        return

    delete_query = "DELETE FROM user_accounts WHERE user_id = %s"
    cursor.execute(delete_query, (user_id,))

    conn.commit()

    print("User account deleted")

def acc_list():
    print("*" * 10,"USERS ACCOUNT LIST","*" * 10)
    
    cursor.execute("SELECT id, user_id, account_no, first_name, last_name, balance FROM user_accounts")
    accounts = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["ID", "User ID", "Account No", "First Name", "Last Name", "Balance"]

    for account in accounts:
        table.add_row(account)

    print(table)

def deposit(user):
    print("*" * 10,"DEPOSIT","*" * 10)
    cursor.execute("SELECT balance FROM user_accounts WHERE user_id = %s", (user[1],))
    current_balance = cursor.fetchone()[0]

    userdeposit = Decimal(input("Enter a deposit amount: "))

    if userdeposit > 0:
        new_balance = Decimal(current_balance + userdeposit)
        update_balance(user[1], new_balance)
        update_transaction_history(user[1], "Deposited successfully", userdeposit)
        
        print(f"Amount deposited successfully. New Balance: {new_balance:.2f}")
    else:
        print("Invalid deposit amount")

def withdraw(user):
    print("*" * 10,"WITHDRAW","*" * 10)
    cursor.execute("SELECT balance FROM user_accounts WHERE user_id = %s", (user[1],))
    current_balance = cursor.fetchone()[0]

    userwithdraw = Decimal(input("Enter an amount to withdraw: "))

    if userwithdraw <= current_balance:
        new_balance = Decimal(current_balance - userwithdraw)
        update_balance(user[1], new_balance)
        update_transaction_history(user[1], "Withdrawn successfully", userwithdraw)

        print("Balance withdrawal successful")
    else:
        print("Insufficient Funds")

def update_transaction_history(user_id, remarks, amount):
    try:
        insert_query = """
        INSERT INTO transaction_history (user_id, remarks, amount)
        VALUES (%s, %s, %s)
        """
        data = (user_id, remarks, amount)
        cursor.execute(insert_query, data)
        conn.commit()
        print(f"Transaction history updated for user_id {user_id}")
    except mysql.connector.Error as e:
        print(f"Error updating transaction history: {e}")

def check_balance(user):
    print("*" * 10,"CHECK BALANCE","*" * 10)
    cursor.execute("SELECT balance FROM user_accounts WHERE user_id = %s", (user[1],))
    result = cursor.fetchone()

    if result is not None:
        current_balance = result[0]
        print(f"Your Balance: {current_balance:.2f}")
    else:
        print("User not found or balance data missing")

def update_balance(user_id, new_balance):
    try:
        cursor.execute("UPDATE user_accounts SET balance = %s WHERE user_id = %s", (new_balance, user_id))
        conn.commit()
        print(f"Updating balance for user_id {user_id} to {new_balance:.2f}")
    except mysql.connector.Error as e:
        print(f"Error updating balance: {e}")

def transaction_history(user):
    print("*" * 10,"TRANSACTION HISTORY","*" * 10)
    user_id = user[1]

    try:
        cursor.execute("SELECT th.transaction_date, th.remarks, th.amount, ua.first_name, ua.last_name, ua.account_no, ua.balance "
                       "FROM transaction_history th "
                       "JOIN user_accounts ua ON th.user_id = ua.user_id "
                       "WHERE ua.user_id = %s", (user_id,))
        transactions = cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["Transaction Date", "Remarks", "Amount", "First Name", "Last Name", "Account No",]

        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[2], transaction[3], transaction[4], transaction[5]])

        print(table)
    except mysql.connector.Error as e:
        print(f"Error fetching transaction history: {e}")

try: 
    while True:
        try:
            print("*" * 10,"MAIN MENU","*" * 10)
            print("*" * 8,"CHOOSE OPTION","*" * 8)
            print("1. Admin ")
            print("2. User ")
            print("3. Exit ")
 
            choice = int(input("Choice: "))
        except:
            print("*" * 10,"CHOOSE VALID NUMERICAL OPTION!","*" * 10)
            continue

        if choice == 1:
            print("*" * 10,"CHOOSE OPTION","*" * 10)
            print("1. Login Now")
            print("2. Back")

            admin_choice = int(input("Choice: "))

            if admin_choice == 1:
                admin_data = admin()
                if admin_data:
                    while True:
                        print("*" * 10,"CHOOSE OPTION","*" * 10)
                        print("1. Create a User Account")
                        print("2. Create an Admin Account")
                        print("3. Update User Details")
                        print("4. Delete User Details")
                        print("5. Show User Details")
                        print("6. Exit")

                        admin_choice = int(input("Choice: "))

                        if admin_choice == 1:
                            create_user_ac(admin_data)
                        elif admin_choice == 2:
                            create_admin_ac(admin_data)
                        elif admin_choice == 3:
                            update_user_detail(admin_data)
                        elif admin_choice == 4:
                            delete_user_details(admin_data)
                        elif admin_choice == 5:
                            acc_list()
                        elif admin_choice == 6:
                            print("*" * 10,"THANK YOU","*" * 10)
                            break
                        else:
                            print("Invalid Selection")
            elif admin_choice == 2:
                continue
            else:
                print("Invalid Selection")
        elif choice == 2:
            print("*" * 10,"CHOOSE OPTION","*" * 10)
            print("1. Login Now")
            print("2. Back")
            
            user_choice = int(input("Choice: "))
            
            if user_choice == 1:
                user_data = user()
                if user_data:
                    while True:
                        print("*" * 10,"CHOOSE OPTION","*" * 10)
                        print("1. Withdraw")
                        print("2. Deposit")
                        print("3. Check Balance")
                        print("4. Transaction History")
                        print("5. Exit")
                    
                        ch = int(input("Choice: "))
                    
                        if ch == 1: 
                            withdraw(user_data)
                        elif ch == 2:
                            deposit(user_data)
                        elif ch == 3:
                            check_balance(user_data)
                        elif ch == 4:
                            transaction_history(user_data)
                        elif ch == 5:
                            print("*" * 10,"THANK YOU","*" * 10)
                            break
                        else:
                            ("Invalid Selection")
                elif user_choice == 2:
                    continue     
                else:
                    print("Invalid Selection")
            
        elif choice == 3:
            print("*" * 10,"THANK YOU","*" * 10)
            break
        else:
            print("Invalid Selection")

    cursor.close()
    conn.close()
except:
    print("*" * 10,"PLEASE RERUN THE PROCESS!","*" * 10)
