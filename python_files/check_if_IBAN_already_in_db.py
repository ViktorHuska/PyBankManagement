import psycopg2
import psycopg2.extras  # for outputting key-value pairs (in form of dictionary) from the db
import numpy as np



def check_if_IBAN_already_in_db(entry):
    from Account import Account
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

        update_script = """SELECT iban FROM account
                           WHERE iban = %s"""
        insert_value = (entry.IBAN,)
        cur.execute(update_script, insert_value)
        result = cur.fetchone()

        while result:
            entry.IBAN = "DE" + str(np.random.randint(0000000000, 9999999999, dtype=np.int64)) \
                        + "0000" + str(np.random.randint(000000, 999999, dtype=np.int64))
            insert_value = (int(entry.IBAN),)
            cur.execute(update_script, insert_value)
            result = cur.fetchone()

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()  # Closing cursor for db
        if conn is not None:
            conn.close()  # Closing connection to db