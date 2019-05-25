from flask import flash, request
from flask import jsonify
from flask import Flask
from flaskext.mysql import MySQL
import pymysql
import requests
import json

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
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

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
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/subject')
def subject():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM subject")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/subject/<id>')
def subject_id(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM subject WHERE SUBJECT_ID = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/student/<id>/grades')
def student_grade(id):
    try:
        blacklist = requests.get('https://clinic.serveo.net/treatment/debtor')
        for ele in blacklist.json():
            if str(ele['student_Id']) == str(id):
                resp = jsonify("Please pay for the treatment service.")
                resp.status_code = 200
                return resp

        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID,subject.SUBJECT_ID,subject.SUBJECT_NAME,GRADE \
                            FROM course_enroll,subject \
                            WHERE course_enroll.SUBJECT_ID=subject.SUBJECT_ID and ID = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/faculty')
def faculty():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM faculty ")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/faculty-location')
def showFacultyLocation():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT FACULTY_NAME, LOCATION FROM faculty_location, faculty WHERE faculty_location.FACULTY_ID = faculty.FACULTY_ID")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

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
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/payment')
def showPayment():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID, YEAR, TERM, PAYMENT_DATE, STATUS FROM payment, tuition_fee \
                        WHERE payment.TUITION_ID = tuition_fee.TUITION_ID")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/payment/<id>')
def showPaymentById(id):
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT payment.ID, YEAR, TERM, AMOUNT, PAYMENT_DATE, payment.STATUS FROM student, payment, tuition_fee, tuition_of_faculty \
                        WHERE payment.TUITION_ID = tuition_fee.TUITION_ID AND student.FACULTY_ID = tuition_of_faculty.FACULTY_ID\
                        AND payment.ID = %s AND student.ID = %s GROUP BY YEAR, TERM", (id,id))
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/tuition-of-faculty')
def showTuitionOfFaculty():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT FACULTY_NAME, AMOUNT FROM tuition_of_faculty, faculty WHERE tuition_of_faculty.FACULTY_ID = faculty.FACULTY_ID GROUP BY FACULTY_NAME")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)
        
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
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

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
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/moved', methods=['POST'])
def moved():
    try:
        req = request.get_json()
        blackListClinic = requests.get('https://clinic.serveo.net/treatment/debtor')
        blackListLib = requests.get('https://library.localtunnel.me/borrow')
        for ele in blackListClinic.json():
            if ele['student_Id'] == req['ID']:
                resp = jsonify("Please pay for the treatment service or return the book.")
                resp.status_code = 200
                return resp
        for ele in blackListLib.json():
            if ele['MEMBER_ID'] == req['ID']:
                resp = jsonify("Please pay for the treatment service or return the book.")
                resp.status_code = 200
                return resp

        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE student SET STATUS = 'M' WHERE ID = %s", req['ID'])
        cnx.commit()
        resp = jsonify("moved successful!")
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/add', methods=['POST'])
def add():
    try:
        req = request.get_json()
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT FACULTY_ID FROM faculty WHERE FACULTY_NAME = %s", req['FACULTY_NAME'])
        rows = cursor.fetchall()
        facultyId = rows[0]['FACULTY_ID']

        cursor.execute("SELECT MAX(ID) FROM student WHERE FACULTY_ID = 0%s", facultyId)
        rows = cursor.fetchall()
        newID = int(rows[0]['MAX(ID)'])+1
        
        cursor.execute("INSERT student (ID, FIRST_NAME, LAST_NAME, GENDER, BDATE, ADDRESS, STATUS, FACULTY_ID) \
                        VALUES (%s, %s, %s, %s, %s, %s, 'S', 0%s)" \
                        , (newID, req['FIRST_NAME'], req['LAST_NAME'], req['GENDER'], req['BDATE'], req['ADDRESS'], facultyId))
        cnx.commit()
        resp = jsonify("added successful!")
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/allOld')
def allOld():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID FROM payment WHERE TUITION_ID = 1")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)

@app.route('/show-non-graduated')
def showNonGraduated():
    try:
        listId = requests.get('https://reg.serveo.net/allOld')
        blackListClinic = requests.get('https://clinic.serveo.net/treatment/debtor')
        blackListLib = requests.get('https://library.localtunnel.me/borrow')

        result = []
        for ele in listId.json():
            for bk1 in blackListClinic.json():
                if ele['ID']==bk1['student_Id']:
                    result.append({"ID": ele['ID']})
                    break
            for bk2 in blackListLib.json():
                if ele['ID']==bk2['MEMBER_ID']:
                    result.append({"ID": ele['ID']})
                    break

        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        resp = jsonify(result)
        resp.status_code = 200
        cursor.close()
        cnx.close()
        return resp
    except Exception as e:
        print(e)