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

@app.route('/faculty-location')
def showFacultyLocation():
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT FACULTY_NAME, LOCATION FROM faculty_location, faculty WHERE faculty_location.FACULTY_ID = faculty.FACULTY_ID")
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    cnx.close()
    return resp

@app.route('/faculty-location/<facultyId>')
def showFacultyLocationById(facultyId):
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT FACULTY_NAME, LOCATION FROM faculty_location, faculty \
                    WHERE faculty_location.FACULTY_ID = faculty.FACULTY_ID AND faculty.FACULTY_ID = %s", facultyId)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    cnx.close()
    return resp

@app.route('/payment')
def showPayment():
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT ID, payment.TUITION_ID, YEAR, TERM, PAYMENT_DATE, STATUS FROM payment, tuition_fee \
                    WHERE payment.TUITION_ID = tuition_fee.TUITION_ID")
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    cnx.close()
    return resp

@app.route('/payment/<id>')
def showPaymentById(id):
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT ID, AMOUNT, PAYMENT_DATE, STATUS FROM payment, tuition_of_faculty \
                    WHERE payment.TUITION_ID = tuition_of_faculty.TUITION_ID AND ID = %s", id)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    cnx.close()
    return resp

@app.route('/tuition-of-faculty')
def showTuitionOfFaculty():
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT FACULTY_NAME, AMOUNT FROM tuition_of_faculty, faculty WHERE tuition_of_faculty.FACULTY_ID = faculty.FACULTY_ID GROUP BY FACULTY_NAME")
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    cnx.close()
    return resp

@app.route('/tuition-of-faculty/<facultyId>')
def showTuitionOfFacultyById(facultyId):
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT FACULTY_NAME, AMOUNT FROM tuition_of_faculty, faculty \
                    WHERE tuition_of_faculty.FACULTY_ID = faculty.FACULTY_ID AND faculty.FACULTY_ID = %s \
                    GROUP BY FACULTY_NAME", facultyId)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    cnx.close()
    return resp