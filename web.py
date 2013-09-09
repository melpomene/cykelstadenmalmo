#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template
app = Flask(__name__)

DB_PATH = 'db.sql'

@app.route("/old")
def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT tweet_id, tweet, time from tweets ORDER BY tweet_id')
    res = []
    for row in c:
        # 2013-08-07 08:33:08
        if datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S" ) > datetime.today() - timedelta(days=31):
            res.append( (row[0], row[1], row[2]))

    amount = len(res)
    return render_template('index.html', amount=amount)

@app.route("/")
@app.route("/list/")
def info():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT tweet_id, tweet, time, url, adress from tweets ORDER BY tweet_id DESC')
    res = []
    for row in c:
        if datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S" ) > datetime.today() - timedelta(days=31):
            res.append( (row[0], row[1], row[2], row[3],row[4]))
    amount = len(res)
    return render_template('list.html', amount=amount, tweets=list(enumerate(res, start=1)))


if __name__ == "__main__":
    app.debug = False 
    app.run(host="0.0.0.0")

