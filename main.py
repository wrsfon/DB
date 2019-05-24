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
    cursor.close()
    cnx.close()
    return resp

@app.route('/student')
def student():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID,FIRST_NAME,LAST_NAME,GENDER,BDATE,ADDRESS,STATUS,faculty.FACULTY_ID,faculty.FACULTY_NAME \
                        FROM student,faculty WHERE student.FACULTY_ID=faculty.FACULTY_ID")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/student/<id>')
def student_id(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID,FIRST_NAME,LAST_NAME,GENDER,BDATE,ADDRESS,STATUS,faculty.FACULTY_ID,faculty.FACULTY_NAME \
                        FROM student,faculty WHERE student.FACULTY_ID=faculty.FACULTY_ID and ID = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/subject')
def subject():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM subject")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/subject/<id>')
def subject_id(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM subject WHERE SUBJECT_ID = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/student/<id>/grades') # check
def student_grade(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID,subject.SUBJECT_ID,subject.SUBJECT_NAME,GRADE \
                        FROM course_enroll,subject \
                        WHERE course_enroll.SUBJECT_ID=subject.SUBJECT_ID and ID = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/faculty')
def faculty():
    cnx = mysql.connect()
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM faculty ")
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    cnx.close()
    return resp