from datetime import datetime
from flask import Flask
from flask import request
import os
import socket
import mysql.connector
import json
import sys

app = Flask(__name__)

cnx = mysql.connector.connect(host="mysqldb",
        user="root",
        password="itmo337980")

print('Server stats:', __name__)

def createDatabase():
    db = cnx.cursor()
    db.execute("CREATE DATABASE IF NOT EXISTS counters")
    print('Database created')
    db.close()

def createTable():
    db = cnx.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS counter (datetime DATETIME, client_info VARCHAR(255))")
    print('Table created')
    db.close()


createDatabase()

cnx = mysql.connector.connect(host="mysqldb",
        user="root",
        password="itmo337980",
        database="counters")

createTable()

def query(query):
    db = cnx.cursor()
    db.execute(query)

    row_headers=[x[0] for x in db.description]

    results = db.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    db.close()

    return json_data

@app.route('/')
def show_counter():
    print('Hello World!', flush=True)
    visits = query('SELECT COUNT(*) as counter FROM counter')
    counter = visits[0]['counter']
    html = "<h3>Счётчик:{counter}</h3>"
    return html.format(counter=counter)

@app.route('/stat')
def inc_counter():
    db = cnx.cursor()
    visits = query('SELECT COUNT(*) as counter FROM counter')
    old_counter = visits[0]['counter']
    db.execute("INSERT INTO counter (datetime, client_info) VALUES (%(datetime)s, %(client_info)s)", 
    { 'datetime': datetime.now(), 'client_info': request.headers.get('User-Agent')})
    html = "<h3>Счётчик:{counter}</h3>"
    return html.format(counter=old_counter)

@app.route("/about")
def hello():
    html = "<h3>Hello, Anna Mokhnatova!</h3><b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

from flask import Flask
app = Flask(__name__)