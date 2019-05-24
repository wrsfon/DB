from flask import flash, request
from flask import jsonify
from flask import Flask
from flaskext.mysql import MySQL
import pymysql
import requests

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'reg'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello_world():
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM student ")
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp

@app.route('/<id>')
def stu(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM student WHERE ID = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()
