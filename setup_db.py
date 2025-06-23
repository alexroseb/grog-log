import sqlite3
import csv

con = sqlite3.connect("grog-log.db")
cur = con.cursor()

def make_drinks():
    cur.execute("DROP TABLE IF EXISTS drinks;")
    con.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS drinks(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    ingredients TEXT
                ); """)
    data = []
    with open('tikisubset.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    cur.executemany("INSERT INTO drinks VALUES(?, ?, ?)", data)
    res = cur.execute("SELECT id, name FROM drinks")
    print(res.fetchall())
    con.commit()

def make_users():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    username TEXT PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    drink_log TEXT
                ); """)
    con.commit()