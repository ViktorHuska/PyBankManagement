import datetime
import psycopg2
from encryption import encryption1_caesar, encryption2_vigenere
from password_check import password_check
import numpy as np


class Account:
    def __init__(self, first_name: str, last_name: str, nationality: str,
                 password: str, DOB, account_type="standard", PIN=None,
                 id=None, IBAN=None):
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.DOB = DOB
        self.balance = 0
        self.account_type = account_type
        self.date_entered = datetime.datetime.now()
        self.password = password

        if IBAN is None:
            self.IBAN = "DE" + str(np.random.randint(0000000000, 9999999999, dtype=np.int64)) \
                        + "0000" + str(np.random.randint(000000, 999999, dtype=np.int64))
        else:
            self.IBAN = IBAN

        if id is None:
            self.ID = np.random.randint(1000000000, 9999999999, dtype=np.int64)
        else:
            self.ID = id

        self.password_error_count = 0
        self.PIN_error_count = 0
        self.error_limit = 4
        # Generation and encryption of PIN
        if PIN is None:
            self.PIN = np.random.randint(1000, 9999)
            self.PIN = encryption1_caesar(str(self.PIN))
            self.PIN = encryption2_vigenere(str(self.PIN))
        else:
            self.PIN = PIN

    # Update personal details, with choices what to change
    def update_personal_details(self):
        from main import account_navigation
        from Security import check_validity_password
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur = None
            change_choice = input("Choose a desired info to change:\n\n"
                                  "==================================================\n"
                                  "============== a) Change password ================\n"
                                  "============== b) Change PIN =====================\n"
                                  "============== c) Change first name ==============\n"
                                  "============== d) Change last name ===============\n"
                                  "============== e) Change nationality =============\n"
                                  "============== f) Change DOB =====================\n"
                                  "==================================================\n\n")
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                cur = conn.cursor()  # Opening cursor for db (helps us to perform operations)

                if change_choice == "a":  # a) Change password
                    # Input and decryption of old password to check validity
                    check_password = check_validity_password(self)

                    if check_password:  # If old password matches to the one registered in DB
                        update_script = """UPDATE account SET password = %s
                                           WHERE id = %s"""

                        password = password_check()  # Insert new password with necessary checks (password must be strong)
                        repeat_password = input(
                            "Repeat your new password: ")  # Must enter new password 2 times and ensure that they match.

                        # Otherwise, need to repeat entering new password again 2 times.
                        while repeat_password != password:
                            print("Password do not match.\n"
                                  "Repeat again!")
                            password = password_check()  # Insert new password with necessary checks
                            repeat_password = input("Repeat your new password: ")

                        password = encryption1_caesar(password)
                        password = encryption2_vigenere(password)
                        insert_values = (password, self.ID)
                        cur.execute(update_script, insert_values)
                    else:
                        if cur is not None:
                            cur.close()  # Closing cursor for db
                        if conn is not None:
                            conn.close()  # Closing connection to db
                        self.access_support()

                if change_choice == "b":  # b) Change PIN
                    # Input and decryption of old PIN to check validity
                    check_PIN = check_validity_password(self)
                    new_pin = input("Input your new PIN, must be exactly 4 number PIN")  # Insert new PIN

                    if check_PIN:  # If old PIN matches to the one registered in DB
                        update_script = """UPDATE account SET pin = %s 
                                           WHERE id = %s"""
                        repeat_pin = input("Repeat your new pin: ")

                        while repeat_pin != new_pin and new_pin != 4:  # Otherwise, need to repeat entering new PIN again 2 times.
                            print("PINs do not match, or it is too long/short.\n"
                                  "Repeat again!")
                            new_pin = input(
                                "Input your new PIN, must be exactly 4 number PIN")  # Insert new PIN with necessary checks
                            repeat_pin = input("Repeat your new PIN: ")

                        insert_values = (new_pin, self.ID)
                        cur.execute(update_script, insert_values)
                        print("Your PIN was successfully changed!\n")
                    else:
                        if cur is not None:
                            cur.close()  # Closing cursor for db
                        if conn is not None:
                            conn.close()  # Closing connection to db
                        self.access_support()

                if change_choice == "c":  # c) Change first name
                    check_password = check_validity_password(self)
                    new_first_name = input("Input your new first name: ")

                    if check_password:  # If password matches to the one registered in DB
                        update_script = """UPDATE account SET first_name = %s 
                                           WHERE id = %s"""
                        repeat_first_name = input("Repeat your new first name: ")

                        while repeat_first_name != new_first_name:
                            print("First names do not match.\n"
                                  "Repeat again!")
                            new_first_name = input("Input your new first name: ")
                            repeat_first_name = input("Repeat your new first name: ")
                        insert_values = (new_first_name, self.ID)
                        cur.execute(update_script, insert_values)
                        print("Your first name was successfully changed!\n")
                    else:
                        if cur is not None:
                            cur.close()  # Closing cursor for db
                        if conn is not None:
                            conn.close()  # Closing connection to db
                        self.access_support()

                if change_choice == "d":  # d) Change last name
                    check_password = check_validity_password(self)
                    new_last_name = input("Input your new last name: ")

                    if check_password:  # If password matches to the one registered in DB
                        update_script = """UPDATE account SET last_name = %s 
                                                           WHERE id = %s"""
                        repeat_last_name = input("Repeat your new last name: ")

                        while repeat_last_name != new_last_name:
                            print("First names do not match.\n"
                                  "Repeat again!")
                            new_last_name = input("Input your new last name: ")
                            repeat_last_name = input("Repeat your new last name: ")
                        insert_values = (new_last_name, self.ID)
                        cur.execute(update_script, insert_values)
                        print("Your last name was successfully changed!\n")
                    else:
                        if cur is not None:
                            cur.close()  # Closing cursor for db
                        if conn is not None:
                            conn.close()  # Closing connection to db
                        self.access_support()

                if change_choice == "e":  # e) Change nationality
                    check_password = check_validity_password(self)
                    new = input("Input your new nationality: ")

                    if check_password:  # If password matches to the one registered in DB
                        update_script = """UPDATE account SET nation = %s 
                                                           WHERE id = %s"""
                        repeat_new = input("Repeat your new nationality: ")

                        while repeat_new != new:
                            print("Nationalities do not match.\n"
                                  "Repeat again!")
                            new = input("Input your new nationality: ")
                            repeat_new = input("Repeat your new nationality: ")
                        insert_values = (new, self.ID)
                        cur.execute(update_script, insert_values)
                        print("Your nationality was successfully changed!\n")
                    else:
                        if cur is not None:
                            cur.close()  # Closing cursor for db
                        if conn is not None:
                            conn.close()  # Closing connection to db
                        self.access_support()

                if change_choice == "f":  # f) Change DOB
                    check_password = check_validity_password(self)
                    time_str = input("Input your new date of birth (yyyy-mm-dd)\n"
                                     "(if month, or day is less than 10, input without zeros at the start): ")
                    new = datetime.datetime.strptime(time_str, "%Y-%m-%d")

                    if check_password:  # If password matches to the one registered in DB
                        update_script = """UPDATE account SET dob = %s 
                                           WHERE id = %s"""
                        time_str = input("Repeat your new date of birth (yyyy-mm-dd)\n"
                                         "(if month, or day is less than 10, input without zeros at the start): ")
                        repeat_new = datetime.datetime.strptime(time_str, "%Y-%m-%d")

                        while repeat_new != new:
                            print("DOBs do not match.\n"
                                  "Repeat again!")

                            time_str = input("Input your new date of birth (yyyy-mm-dd)\n"
                                             "(if month, or day is less than 10, input without zeros at the start): ")
                            new = datetime.datetime.strptime(time_str, "%Y-%m-%d")

                            time_str = input("Repeat your new date of birth (yyyy-mm-dd)\n"
                                             "(if month, or day is less than 10, input without zeros at the start): ")
                            repeat_new = datetime.datetime.strptime(time_str, "%Y-%m-%d")
                        insert_values = (new, self.ID)
                        cur.execute(update_script, insert_values)
                        print("Your DOB was successfully changed!\n")
                    else:
                        if cur is not None:
                            cur.close()  # Closing cursor for db
                        if conn is not None:
                            conn.close()  # Closing connection to db
                        self.access_support()

                conn.commit()

            except Exception as error:
                print(error)
                conn.rollback()
            finally:
                if cur is not None:
                    cur.close()  # Closing cursor for db
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(id=self.ID)
        else:
            account_navigation(id=self.ID)

    # Deposit money to account
    def deposit_money(self):
        from main import account_navigation
        from Security import check_validity_PIN
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur1 = None
            cur2 = None
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                check_pin = check_validity_PIN(self)
                new = input("How much money you want to deposit: ")

                if check_pin:  # If password matches to the one registered in DB
                    cur1 = conn.cursor()
                    cur2 = conn.cursor()
                    balance_check_script = """SELECT balance FROM account
                                              WHERE iban = %s"""
                    update_script = """UPDATE account SET balance = %s 
                                       WHERE iban = %s"""
                    user = (self.IBAN,)
                    cur1.execute(balance_check_script, user)
                    balance = cur1.fetchone()[0]
                    new_balance = balance + int(new)

                    insert_values = (new_balance, self.IBAN)
                    cur2.execute(update_script, insert_values)

                    cur1.execute(balance_check_script, (user,))
                    final_balance = cur1.fetchone()[0]
                    conn.commit()
                    print(f"Deposit was successful!\n"
                          f"Current money: {final_balance} euros")
                else:
                    if conn is not None:
                        conn.close()  # Closing connection to db
                    self.access_support()

            except Exception as error:
                print(error)
                conn.rollback()
            finally:
                if cur1 is not None:
                    cur1.close()  # Closing cursor for db
                if cur2 is not None:
                    cur2.close()  # Closing cursor for db
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(id=self.ID)
        else:
            account_navigation(id=self.ID)

    # Withdraw money, requires PIN
    def withdraw_money(self):
        from main import account_navigation
        from Security import check_validity_PIN
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur1 = None
            cur2 = None
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                check_pin = check_validity_PIN(self)
                cur1 = conn.cursor()
                cur2 = conn.cursor()

                balance_check_script = """SELECT balance FROM account
                                          WHERE id = %s"""
                user = (self.ID,)
                cur1.execute(balance_check_script, user)
                balance = cur1.fetchone()[0]
                new = int(input(f"Current balance: {balance} euros\n"
                                "How much money you want to withdraw: "))

                if check_pin:  # If password matches to the one registered in DB
                    update_script = """UPDATE account SET balance = %s 
                                       WHERE id = %s"""
                    insert_values = (balance - new, self.ID)
                    while balance < new:
                        choice = int(input("There is not enough money on your account for withdrawal.\n"
                                           f"Current balance is {self.balance} euros.\n"
                                           "Please, choose another sum, or you can go to the main screen: \n\n"
                                           "a) Choose another sum\n"
                                           "b) Go to the main screen"))
                        if choice == "a":
                            new = int(input(f"Current balance: {self.balance} euros.\n"
                                            "Excellent, please, choose the sum for withdrawal: "))
                        if choice == "b":
                            if cur1 is not None:
                                cur1.close()
                            if cur2 is not None:
                                cur2.close()  # Closing cursor for db
                            if conn is not None:
                                conn.close()  # Closing connection to db
                            account_navigation(id=self.ID)
                    cur2.execute(update_script, insert_values)
                    conn.commit()
                    cur1.execute(balance_check_script, user)
                    balance = cur1.fetchone()[0]
                    print(f"Withdrawal was successful!\n"
                          f"Current money: {balance} euros")
                else:
                    self.access_support()

            except Exception as error:
                print(error)
                conn.rollback()
            finally:
                if cur1 is not None:
                    cur1.close()
                if cur2 is not None:
                    cur2.close()  # Closing cursor for db
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(id=self.ID)
        else:
            account_navigation(id=self.ID)

    # Checks balance of account
    def check_balance(self):
        from main import account_navigation
        from Security import check_validity_PIN
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur = None
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                cur = conn.cursor()
                check_pin = check_validity_PIN(self)

                if check_pin:  # If password matches to the one registered in DB
                    search_script = """SELECT balance FROM account
                                       WHERE id = %s"""
                    insert_values = (self.ID,)
                    cur.execute(search_script, insert_values)
                    result = cur.fetchone()
                    print(f"Current balance is {result[0]} euros\n")
                else:
                    self.access_support()
            except Exception as error:
                print(error)
                conn.rollback()
            finally:
                if cur is not None:
                    cur.close()  # Closing cursor for db
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(id=self.ID)
        else:
            account_navigation(id=self.ID)

    # Make money transaction from my account to another, with the help of Account_ID, requires PIN
    def make_transaction(self):  # Make transaction to another account, requires PIN
        from main import account_navigation
        from Security import check_validity_PIN
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur1 = None
            cur2 = None
            cur3 = None
            cur4 = None
            cur5 = None
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                check_pin = check_validity_PIN(self)
                cur1 = conn.cursor()
                # For cur1
                balance_check_script = """SELECT balance FROM account
                                             WHERE id = %s"""
                user = (self.ID,)
                cur1.execute(balance_check_script, user)
                balance = cur1.fetchone()[0]
                IBAN = input(f"Current balance: {balance} euros\n"
                                 "To whome do you want to send money? Enter IBAN: ")
                new = int(input("How much money do you want to send: "))

                while True:
                    c = input(f"Did you enter IBAN correctly? {IBAN}\n"
                              f"Do you confirm?\n\n"
                              f"y) Yes\n"
                              f"n) No\n"
                              f"b) Go back to main menu\n\n")
                    if c == "y":
                        break
                    if c == "n":
                        IBAN = int(input(f"Enter IBAN of receiver: "))
                        continue
                    if c == "b":
                        account_navigation(id=self.ID)

                cur2 = conn.cursor()
                cur3 = conn.cursor()
                cur4 = conn.cursor()
                cur5 = conn.cursor()

                if check_pin:  # If password matches to the one registered in DB
                    # =========================================================================================================
                    # For cur2
                    update_balance_script = """UPDATE account SET balance = %s 
                                          WHERE id = %s"""
                    # For cur3
                    check_balance_receiver = """SELECT balance, id FROM account
                                             WHERE iban = %s"""
                    # For cur5
                    make_record_of_transaction = """INSERT INTO transactions(transaction_sum, receiver_id, sender_id)
                                                    VALUES (%s, %s, %s)"""
                    # =========================================================================================================
                    insert_values3 = (IBAN,)
                    cur3.execute(check_balance_receiver, insert_values3)
                    receiver_balance = cur3.fetchone()
                    print(type(receiver_balance))

                    while balance < new:
                        choice = input("There is not enough money on your account for withdrawal.\n"
                                           f"Current balance is {balance} euros.\n"
                                           "Please, choose another sum, or you can go to the main screen: \n\n"
                                           "a) Choose another sum\n"
                                           "b) Go to the main screen\n\n")
                        if choice == "a":
                            new = int(input(f"Current balance: {balance} euros.\n"
                                            "Excellent, please, choose the sum for withdrawal: "))
                        if choice == "b":
                            if cur1 is not None:
                                cur1.close()
                            if cur2 is not None:
                                cur2.close()
                            if cur3 is not None:
                                cur3.close()
                            if cur4 is not None:
                                cur4.close()
                            if cur5 is not None:
                                cur5.close()
                            if conn is not None:
                                conn.close()  # Closing connection to db
                            account_navigation(id=self.ID)
                    # Updating balance of sender and receiver
                    # ==================================================================
                    insert_values2 = (balance - new, self.ID)
                    insert_values4 = (receiver_balance[0] + new, receiver_balance[1])
                    cur2.execute(update_balance_script, insert_values2)
                    cur4.execute(update_balance_script, insert_values4)
                    # ==================================================================
                    # Insert information about transaction into transactions table
                    insert_values5 = (new, receiver_balance[1], self.ID)
                    cur5.execute(make_record_of_transaction, insert_values5)
                    conn.commit()
                    cur1.execute(balance_check_script, user)
                    balance = cur1.fetchone()[0]
                    print(f"Transfer was done successfully! Your current balance is: {balance}")
                else:
                    self.access_support()

            except Exception as error:
                print(error)
                conn.rollback()
            finally:
                if cur1 is not None:
                    cur1.close()
                if cur2 is not None:
                    cur2.close()
                if cur3 is not None:
                    cur3.close()
                if cur4 is not None:
                    cur4.close()
                if cur5 is not None:
                    cur5.close()
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(id=self.ID)
        else:
            account_navigation(id=self.ID)

    # Check all transactions for certain period of time, requires PIN
    def check_all_transactions(self):
        from main import account_navigation
        from Security import check_validity_PIN
        from datetime import datetime, timedelta
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur1 = None
            cur2 = None
            cur3 = None
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                check_pin = check_validity_PIN(self)
                # For cur1
                transactions_output_script_7days = """SELECT * FROM transactions
                                                      WHERE (sender_id = %s OR receiver_id = %s) AND date >= %s"""

                transactions_output_script_30days = """SELECT * FROM transactions
                                                       WHERE (sender_id = %s OR receiver_id = %s) AND date >= %s"""

                transactions_output_script_alltime = """SELECT * FROM transactions
                                                        WHERE sender_id = %s OR receiver_id = %s"""
                convert_id_into_IBAN_script = """SELECT iban FROM account
                                                 WHERE id = %s"""

                if check_pin:  # If password matches to the one registered in DB
                    cur1 = conn.cursor()
                    cur2 = conn.cursor()
                    cur3 = conn.cursor()
                    time_period = input("Choose desired time, for which you want to see all your transactions: \n\n"
                                        "a) 7 days\n"
                                        "b) 30 days\n"
                                        "c) All time\n")
                    result = []

                    if time_period == "a":
                        start_date = datetime.now() - timedelta(days=7)
                        insert_values1 = (self.ID, self.ID, start_date)
                        cur1.execute(transactions_output_script_7days, insert_values1)
                        result = cur1.fetchall()
                    if time_period == "b":
                        start_date = datetime.now() - timedelta(days=30)
                        insert_values1 = (self.ID, self.ID, start_date)
                        cur1.execute(transactions_output_script_30days, insert_values1)
                        result = cur1.fetchall()
                    if time_period == "c":
                        insert_values1 = (self.ID, self.ID)
                        cur1.execute(transactions_output_script_alltime, insert_values1)
                        result = cur1.fetchall()

                    # From result, take out id of sender and receiver and get IBANs from both.
                    # Afterwards, replace ids with IBANs.
                    insert_values2 = (result[0][2],)  # receiver ID
                    insert_values3 = (result[0][3],)  # sender ID

                    cur2.execute(convert_id_into_IBAN_script, insert_values2)
                    receiver_IBAN = cur2.fetchone()[0]

                    cur3.execute(convert_id_into_IBAN_script, insert_values3)
                    sender_IBAN = cur3.fetchone()[0]
                    results = []
                    r = []
                    for t in result:
                        results.append(r)
                        for j in t:
                            r.append(j)

                    for transaction in results:  # Reason for this loop is to check cases if receiver_ID doesn't match our account ID,
                        # then our Account sent this transaction, if sender ID doesn't match our account ID,
                        # then our account received the transaction
                        if transaction[2] == self.ID:
                            transaction[2] = sender_IBAN
                        else:
                            transaction[2] = receiver_IBAN
                        if transaction[3] == self.ID:
                            transaction[3] = sender_IBAN
                        else:
                            transaction[3] = receiver_IBAN
                    print("List of transactions\n"
                          "id, amount, receiver_IBAN, sender_IBAN, date")
                    for row in results:
                        print(row)
                else:
                    self.access_support()

            except Exception as error:
                print(error)
                conn.rollback()
            finally:
                if cur1 is not None:
                    cur1.close()
                if cur2 is not None:
                    cur2.close()
                if cur3 is not None:
                    cur3.close()
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(id=self.ID)
        else:
            account_navigation(id=self.ID)

    # Will return bank support contact details
    def access_support(self):
        from main import account_navigation
        print("==========================================================")
        print("===== Contact to the E-Bank: =============================\n\n"
              "=============== 1)Name: Mike Meier =======================\n"
              "================= Phone: +4917989564024 ==================\n"
              "================= Email: E-Bank1@gmail.com ===============\n"
              "==========================================================\n"
              "================= Working hours: 8:00 - 16:00 ============\n"
              "================= Working days: Mon - Sat ================\n\n")
        print("=============== 2)Name: Nadia Muller =====================\n"
              "================= Phone: +4918912577718 ==================\n"
              "================= Email: E-Bank2@gmail.com ===============\n"
              "==========================================================\n"
              "================= Working hours: 11:00 - 19:00 ===========\n"
              "================= Working days: Mon - Sat ================\n\n")
        print("=============== 3)Name: Killian Jones ====================\n"
              "================= Phone: +4916127024015 ==================\n"
              "================= Email: E-Bank3@gmail.com ===============\n"
              "==========================================================\n"
              "================= Working hours: 8:00 - 20:00 ============\n"
              "================= Working days: Mon - Friday =============\n\n")
        print("== Feel free to contact any person from the list above, ==\n"
              "=== or address to the nearest bank department location ===\n")
        print("==========================================================")
        input("When you are ready to proceed to starting menu, enter any symbol and press enter\n")
        account_navigation(id=self.ID)

    # Logoff of the account
    def logoff(self):
        from main import starting_menu
        starting_menu()

    # Delete account
    def delete_account(self):
        from main import account_navigation, starting_menu
        from Security import check_validity_PIN, check_validity_password
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur = None
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                cur = conn.cursor()
                check_pin = check_validity_PIN(self)
                check_password = check_validity_password(self)

                if check_pin and check_password:  # If password and pin match to the ones registered in DB
                    choice = input("Are you sure you want to proceed with deletion of your account?\n\n"
                                   "y) Yes\n"
                                   "n) No\n")
                    if choice == "y":
                        deletion_script = """DELETE FROM account
                                             WHERE id = %s"""
                        insert_values = (self.ID,)
                        cur.execute(deletion_script, insert_values)
                        conn.commit()
                        print(f"Your account was successfully deleted!\n")
                    if choice == "n":
                        if cur is not None:
                            cur.close()  # Closing cursor for db
                        if conn is not None:
                            conn.close()  # Closing connection to db
                        account_navigation(self.ID)

                else:
                    self.access_support()
            except Exception as error:
                print(error)
                conn.rollback()
            finally:
                if cur is not None:
                    cur.close()  # Closing cursor for db
                if conn is not None:
                    conn.close()  # Closing connection to db
                starting_menu()
        else:
            account_navigation(id=self.ID)

    # Print out all general info about my account
    def account_info(self):
        from main import account_navigation
        from Security import check_validity_PIN
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            hostname = 'localhost'
            database = 'Bank_Management_System'
            username = 'postgres'
            pwd = 'pass'
            port_id = 5433

            conn = None
            cur = None
            try:
                conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                        dbname=database,
                                        user=username,
                                        password=pwd,
                                        port=port_id)

                check_pin = check_validity_PIN(self)

                if check_pin:  # If password and pin match to the ones registered in DB
                    cur = conn.cursor()
                    search_script = """SELECT * FROM account
                                       WHERE id = %s"""
                    insert_value = (self.ID,)
                    cur.execute(search_script, insert_value)
                    info = cur.fetchone()
                    print(info)
                    labels = ["id", "first_name", "last_name", "nationality", "DOB", "balance", "password", "account_type", "date_entered", "PIN", "IBAN"]
                    print("Info about account\n\n")
                    for i in range(len(info)):
                        if type(info[i]) != datetime:
                            print(f"{labels[i]} : {info[i]}")
                        if type(i) == datetime:
                            # Format the datetime object as a string
                            formatted_date = info[i].strftime("%Y-%m-%d %H:%M:%S")
                            print(f"{labels[i]} : {formatted_date}")
                else:
                    self.access_support()
            except Exception as error:
                print(error)
            finally:
                if cur is not None:
                    cur.close()  # Closing cursor for db
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(id=self.ID)
        else:
            account_navigation(id=self.ID)
