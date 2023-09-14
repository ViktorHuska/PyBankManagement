import os
import sys
import datetime
import psycopg2


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.flush()  # Flush the output buffer


# Main menu of bank account when logged in
def account_navigation(id):
    from Account import Account
    print("=================================================================\n"
          "=============Welcome to your E-Bank account cabinet==============\n"
          "=================================================================\n"
          "a) Check your balance\n"
          "b) Deposit money\n"
          "c) Withdraw money\n"
          "d) Update personal info\n"
          "e) Make Transaction\n"
          "f) Check all transactions\n"
          "g) Access support\n"
          "h) Delete account\n"
          "i) Logoff\n"
          "j) Account info\n"
          "================================================================\n\n")

    hostname = 'localhost'
    database = 'Bank_Management_System'
    username = 'postgres'
    pwd = 'pass'
    port_id = 5433

    conn = None
    cur = None
    cur2 = None

    try:
        conn = psycopg2.connect(host=hostname,  # Establishing connection to db
                                dbname=database,
                                user=username,
                                password=pwd,
                                port=port_id)

        cur = conn.cursor()
        cur2 = conn.cursor()

        choice = input("Choose desired operation: ")
        search_account_info_script = """SELECT * FROM account WHERE id = %s"""
        insert_value = (id,)

        cur.execute(search_account_info_script, insert_value)
        info = cur.fetchall()

        # Get column names from cursor description
        column_names = [desc[0] for desc in cur.description]
        # Obtain key-value pairs for each variable
        row_dict = {}
        for row in info:
            row_dict = dict(zip(column_names, row))

        id = row_dict["id"]
        first_name = row_dict["first_name"]
        last_name = row_dict["last_name"]
        nationality = row_dict["nation"]
        DOB = row_dict["dob"]
        account_type = row_dict["account_type"]
        password = row_dict["password"]
        pin = row_dict["pin"]
        IBAN = row_dict["iban"]


        account = Account(first_name=first_name, last_name=last_name,  # Creation of account
                              nationality=nationality, DOB=DOB,
                              password=password, account_type=account_type,
                              PIN=pin, id=id, IBAN=IBAN)

        if choice == "a": # Check your balance
            account.check_balance()

        if choice == "b": # Deposit money to the account
            account.deposit_money()

        if choice == "c": # Withdraw money from the account
            account.withdraw_money()

        if choice == "d": # Update personal details
            account.update_personal_details()

        if choice == "e": # Make transaction to [userIBAN]
            account.make_transaction()

        if choice == "f": # Check all transactions (for certain period of time)
            account.check_all_transactions()

        if choice == "g": # Access support
            account.access_support()

        if choice == "h": # Delete account
            account.delete_account()

        if choice == "i": # Logoff
            if cur is not None:
                cur.close()
            if cur2 is not None:
                cur2.close()
            if conn is not None:
                conn.close()
            account.logoff()

        if choice == "j": # Print out all info about account
            account.account_info()


    except Exception as error:
        print(error)
        conn.rollback()
    finally:
        if cur is not None:
            cur.close()  # Closing cursor for db
        if cur2 is not None:
            cur2.close()  # Closing cursor for db
        if conn is not None:
            conn.close()  # Closing connection to db
        account_navigation(id)



def starting_menu():
    from Account import Account
    from encryption import encryption1_caesar, encryption2_vigenere, decryption1_vigenere, decryption2_caesar
    from password_check import password_check
    from insert_entries_into_db import insert_entries_into_db
    from check_if_ID_already_in_db import check_if_ID_already_in_db
    from check_if_IBAN_already_in_db import check_if_IBAN_already_in_db
    print("========================================================")
    print("================Welcome to the bank menu================")
    print("===========Log into your account, or register===========")
    print("========= a) Log in ====================================")
    print("========= b) Register ==================================")
    print("========= c) Exit ======================================")
    print()
    choice = input("Please, choose desired option - a), b) or c) \n")
    if choice == "a":  # Log into account
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

                cur1 = conn.cursor()
                cur2 = conn.cursor()
                login = input("Enter your login:")  # login will be as "ID" of an account
                password = input("Enter your password:")
                while login == "" or password == "":
                    print("Your login or password was empty, try again.")
                    login = input("Enter your login:")
                    password = input("Enter your password:")

                login_search_script = """SELECT id FROM account WHERE id = %s"""
                password_search_script = """SELECT password FROM account WHERE id = %s"""

                insert_values1 = (int(login),)
                cur1.execute(login_search_script, insert_values1)
                row_dict = []
                login_result = cur1.fetchone()

                # If login not in the db, then retry. Input everything once again

                while not login_result[0]:
                    print("Login or password was incorrect! Try again.")
                    login = input("Enter your login:")
                    password = input("Enter your password:")
                    insert_values1 = (int(login),)
                    cur1.execute(login_search_script, insert_values1)
                    login_result = cur1.fetchone()

                # If eventually some account id was found in the DB, then look for password for that account

                insert_values2 = (int(login_result[0]),)
                cur2.execute(password_search_script, insert_values2)
                password_result = cur2.fetchone()

                #Decrypt password back from DB
                password_result = decryption1_vigenere(password_result[0])
                password_result = decryption2_caesar(password_result)


                # If the password for that account is not correct, then ask to retry entering all info once again

                while password != password_result:
                    print("Login or password was incorrect! Try again.")
                    login = input("Enter your login:")
                    password = input("Enter your password:")
                    insert_values1 = (int(login),)
                    cur1.execute(login_search_script, insert_values1)
                    login_result = cur1.fetchone()
                    if login_result is None:                # if once again, there is no such such ID in DB,
                                                            # then ask for info again (useless to look for password)
                        continue
                    insert_values2 = (int(login_result[0]),)   # Look for password and then at the end, the while loop will compare the password
                                                            # for the userID and the password that was entered
                    cur2.execute(password_search_script, insert_values2)
                    password_result = cur2.fetchone()

                    password_result = decryption1_vigenere(password_result[0])
                    password_result = decryption2_caesar(password_result)
            except Exception as error:
                print(error)
                if cur1 is not None:
                    cur1.close()  # Close the cursor
                if cur2 is not None:
                    cur2.close()  # Close the cursor
                conn.rollback()
                if conn is not None:
                    conn.close()  # Close the connection
                print("Something went wrong, try again!")
                starting_menu()
            finally:
                if cur1 is not None:
                    cur1.close()  # Closing cursor for db
                if cur2 is not None:
                    cur2.close()  # Closing cursor for db
                if conn is not None:
                    conn.close()  # Closing connection to db
                account_navigation(login_result)  # Account page (for user entered) and actions that can be done within
        if choice1 == "b":
            starting_menu()
        # =========================================
        # Pseudo-code for security
        # =========================================
        # Check if the information coincides with the actual information
        # if login not in database:
        #     print("Login or password is not correct!")
        # if database[login] =! password:
        #    print("Login or password is not correct!")

    if choice == "b":  # Registration of a new account
        choice1 = input("Do you want to proceed, or come back to main screen?\n\n"
                        "a) Proceed\n"
                        "b) Come back\n")
        if choice1 == "a":
            print("Try to input your data correctly from the first try! \n"
                  "You will be able to change your personal info only after finishing setting up your account.")

            print()

            first_name = input("Input your first_name: ")
            last_name = input("Input your last_name: ")
            nationality = input("Input your nationality: ")
            time_str = input("Input your date of birth (yyyy-mm-dd)\n"
                             "(if month, or day is less than 10, input without zeros at the start): ")
            DOB = datetime.datetime.strptime(time_str, "%Y-%m-%d")
            account_type = input("Input your desired account type (standard, or premium), write only (s, or p): ")

            # Input and encryption of password
            password = password_check()
            password = encryption1_caesar(password=password)
            password = encryption2_vigenere(password_caesar=password)

            new_Account = Account(first_name=first_name, last_name=last_name,  # Creation of account
                                  nationality=nationality, DOB=DOB,
                                  password=password, account_type=account_type)

            check_if_ID_already_in_db(new_Account)  # If there is already a record with the same ID as the one already existing in the DB,
            #                                         then change it to another one until it is unique.
            check_if_IBAN_already_in_db(new_Account)
            print(
                "========================================================================================================")
            print(
                "=Your account was created successfully, as a login you will have a special number!======================\n"
                "=Save this number! Without it you won't be able to get into your account!===============================\n"
                "=Also, you will get a PIN-code, with it you will be able to make transactions and change personal info.=\n")
            print(
                "========================================================================================================")
            print(
                f"==========================Your login is: {new_Account.ID}, your PIN is: {new_Account.PIN}==================================\n"
                f"==================================Your IBAN is: {new_Account.IBAN}==================================")
            print(
                "========================================================================================================")

            insert_entries_into_db(new_Account)  # Insert entry into DB
            print("\n\n Now you can log into your account!")
            starting_menu()
        else:
            starting_menu()

    if choice == "c":
        return 0


if __name__ == "__main__":
    starting_menu() # Start of program

# TODO: For future, implement password/PIN error count into DB
# TODO: for future, remove transactions to account ID that was deleted
# TODO: Make better GUI for interraction with the bank
# TODO: Create script to clean terminal screen