from flask import Flask, render_template, session, json, request, redirect, flash
import sqlite3
from setup_db import *

app = Flask(__name__)

make_drinks_db()
make_users_db()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<id>")
def drink_info(id):
    con = sqlite3.connect("grog-log.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM drinks WHERE id = ?", id)
    drink_info = res.fetchall()
    print(drink_info)
    if len(drink_info)>0:
        ingredients = drink_info[0][2].split(",")
        return render_template("drink_details.html", id=drink_info[0][0], name=drink_info[0][1], ingredients=ingredients)
    else:
        return render_template("drink_details.html", id=id, name="No drink found", ingredients=[])