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

@app.route('/student/<id>/grades')
def student_grade(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)

        blacklist = requests.get('http://127.0.0.1:5000/notpay')

        status = 1

        for ele in blacklist.json():
            print(ele['ID'])
            if str(ele['ID']) == str(id):
                status = 0
                break

        if(status == 1):
            cursor.execute("SELECT ID,subject.SUBJECT_ID,subject.SUBJECT_NAME,GRADE \
                            FROM course_enroll,subject \
                            WHERE course_enroll.SUBJECT_ID=subject.SUBJECT_ID and ID = %s", id)
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            resp = jsonify("Please pay for the treatment service.")
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/faculty')
def faculty():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM faculty ")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/faculty-location')
def showFacultyLocation():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT FACULTY_NAME, LOCATION FROM faculty_location, faculty WHERE faculty_location.FACULTY_ID = faculty.FACULTY_ID")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/faculty-location/<facultyId>')
def showFacultyLocationById(facultyId):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT FACULTY_NAME, LOCATION FROM faculty_location, faculty \
                        WHERE faculty_location.FACULTY_ID = faculty.FACULTY_ID AND faculty.FACULTY_ID = %s", facultyId)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/payment')
def showPayment():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID, payment.TUITION_ID, YEAR, TERM, PAYMENT_DATE, STATUS FROM payment, tuition_fee \
                        WHERE payment.TUITION_ID = tuition_fee.TUITION_ID")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/payment/<id>')
def showPaymentById(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID, AMOUNT, PAYMENT_DATE, STATUS FROM payment, tuition_of_faculty \
                        WHERE payment.TUITION_ID = tuition_of_faculty.TUITION_ID AND ID = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/tuition-of-faculty')
def showTuitionOfFaculty():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT FACULTY_NAME, AMOUNT FROM tuition_of_faculty, faculty WHERE tuition_of_faculty.FACULTY_ID = faculty.FACULTY_ID GROUP BY FACULTY_NAME")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/tuition-of-faculty/<facultyId>')
def showTuitionOfFacultyById(facultyId):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT FACULTY_NAME, AMOUNT FROM tuition_of_faculty, faculty \
                        WHERE tuition_of_faculty.FACULTY_ID = faculty.FACULTY_ID AND faculty.FACULTY_ID = %s \
                        GROUP BY FACULTY_NAME", facultyId)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/notpay')
def notpay():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID FROM payment\
                        WHERE STATUS = 'N' ")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()
