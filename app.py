from flask import Flask
import sqlite3
from setup_db import *

app = Flask(__name__)
con = sqlite3.connect("grog-log.db")
cur = con.cursor()

make_drinks()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"