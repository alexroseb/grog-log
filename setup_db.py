import sqlite3
import csv

con_setup = sqlite3.connect("grog-log.db")
cur_setup = con_setup.cursor()

def make_drinks_db():
    cur_setup.execute("DROP TABLE IF EXISTS drinks;")
    con_setup.commit()
    cur_setup.execute("""CREATE TABLE IF NOT EXISTS drinks(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    ingredients TEXT
                ); """)
    data = []
    with open('tikisubset.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    cur_setup.executemany("INSERT INTO drinks VALUES(?, ?, ?)", data)
    con_setup.commit()

def make_users_db():
    cur_setup.execute("""CREATE TABLE IF NOT EXISTS users(
                    username TEXT PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    drink_log TEXT
                ); """)
    con_setup.commit()