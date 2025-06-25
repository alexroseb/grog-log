import csv
import os
from psycopg2 import pool
from dotenv import load_dotenv

def make_drinks_db():
    # Load .env file
    load_dotenv()
    # Get the connection string from the environment variable
    connection_string = os.getenv('DATABASE_URL')
    # Create a connection pool
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections in the pool
        10,  # Maximum number of connections in the pool
        connection_string
    )
    # Check if the pool was created successfully
    if connection_pool:
        print("Connection pool created successfully")
    # Get a connection from the pool
    con_setup = connection_pool.getconn()

    # Create a cursor object
    cur_setup = con_setup.cursor()
    data = []
    with open('tikisubset.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)

    # cursor.mogrify() to insert multiple values
    args = ','.join(cur_setup.mogrify("(%s,%s,%s)", i).decode('utf-8')
                    for i in data)

    # executing the sql statement
    cur_setup.execute("INSERT INTO drinks VALUES " + (args))
    con_setup.commit()

    # Close the cursor and return the connection to the pool
    cur_setup.close()
    connection_pool.putconn(con_setup)

    # Close all connections in the pool
    connection_pool.closeall()

make_drinks_db()