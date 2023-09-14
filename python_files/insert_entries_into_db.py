import psycopg2

def insert_entries_into_db(entry):
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
        # To return dictionary from db, we define cursor like that:
        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        insert_script = """INSERT INTO account (id, first_name, last_name, nation, dob, balance, password, account_type, date_entered, pin, IBAN)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        insert_value = (int(entry.ID), entry.first_name, entry.last_name, entry.nationality, entry.DOB,
                        entry.balance, entry.password, entry.account_type, entry.date_entered, entry.PIN, entry.IBAN)
        cur.execute(insert_script, insert_value)  # Input records into the table

        # cur.execute("SELECT * FROM Account")
        # cur.fetchall() # View all data from cursor
        # or cur.fetchone() # View one record of data

        conn.commit()

        # cur.close()  # Closing cursor for db      ###!Not recommended to do it here, because maybe connection and cursor will never be created
        # conn.close()  # Closing connections to db

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()  # Closing cursor for db
        if conn is not None:
            conn.close()  # Closing connection to db
