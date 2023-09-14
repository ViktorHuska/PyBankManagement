from Account import Account
from main import account_navigation, starting_menu
import psycopg2
import psycopg2.extras
from encryption import decryption1_vigenere, decryption2_caesar


# Check if password/PIN is correct
# When password/PIN was written incorrectly 4 times, account is blocked
# and cannot be accessed without contacting support for further actions
def check_validity_password(entry: Account):
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

        cur = conn.cursor()  # Opening cursor for db (helps us to perform operations)
        # To return dictionary from db, we define cursor like that:
        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        while entry.password_error_count < 4:
            choice = input(
                f"You have {entry.error_limit - entry.password_error_count} tries to enter your current password.\n"
                f"Do you want to continue, or go back to starting screen?\n\n"
                f"a) Go to starting screen\n"
                f"b) Enter your current password\n")
            password = input("Try again, input your current password: ")
            search_script = """SELECT password FROM account
                               WHERE id = %s"""
            input_values = (entry.ID,)
            cur.execute(search_script, input_values)
            # Fetch password value from db
            result = cur.fetchone()[0]
            if choice == "a":
                starting_menu()
            if choice == "b":
                result = decryption1_vigenere(result)
                result = decryption2_caesar(result)
                if password == result:
                    entry.password_error_count = 0
                    print("Current password matches!\n")
                    return True
                else:
                    entry.password_error_count += 1
                    print(
                        f"Password is incorrect! You have {entry.error_limit - entry.password_error_count} more tries!")
                    continue
        print("You have used all your tries to enter password, refer to the bank department to restore your account.")
        return False

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()  # Closing cursor for db
        if conn is not None:
            conn.close()  # Closing connection to db


def check_validity_PIN(entry: Account):
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

        cur = conn.cursor()  # Opening cursor for db (helps us to perform operations)
        # To return dictionary from db, we define cursor like that:
        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        while entry.PIN_error_count < 4:
            choice = input(
                f"You have {entry.error_limit - entry.PIN_error_count} tries to enter your PIN.\n"
                f"Do you want to continue, or go back to starting screen?\n\n"
                f"a) Go to starting screen\n"
                f"b) Enter PIN\n")
            PIN = input("Input your PIN(4 numbers): ")
            search_script = """SELECT pin FROM account
                               WHERE id = %s"""
            input_values = (entry.ID,)
            cur.execute(search_script, input_values)
            result_PIN = cur.fetchone()
            if choice == "a":
                account_navigation(entry.ID)
            if choice == "b":
                # result = decryption1_vigenere(result)
                # result = decryption2_caesar(result)
                if PIN == result_PIN[0]:
                    entry.PIN_error_count = 0
                    print("Your PIN matches!\n")
                    return True
                else:
                    entry.PIN_error_count += 1
                    print(f"Your PIN is incorrect! You have {entry.error_limit - entry.PIN_error_count} more tries!")
                    continue
        print("You have used all your tries to enter PIN, refer to the bank department to"
              "restore your full capabilities of an account.")
        return False

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()  # Closing cursor for db
        if conn is not None:
            conn.close()  # Closing connection to db
