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

@app.route('/moved/', methods=['POST'])
def moved():
    try:
        req = request.get_json()
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE student SET STATUS = 'M' WHERE ID = %s", req['ID'])
        cnx.commit()
        resp = jsonify("moved successful!")
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/add', methods=['POST'])
def add():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT MAX(ID) FROM student")
        rows = cursor.fetchall()
        newID = int(rows[0]['MAX(ID)'])+1

        req = request.get_json()
        cursor.execute("SELECT FACULTY_ID FROM faculty WHERE FACULTY_NAME = %s", req['FACULTY_NAME'])
        rows = cursor.fetchall()
        facultyId = rows[0]['FACULTY_ID']
        
        cursor.execute("INSERT student (ID, FIRST_NAME, LAST_NAME, GENDER, BDATE, ADDRESS, STATUS, FACULTY_ID) \
                        VALUES (%s, %s, %s, %s, %s, %s, 'S', 0%s)" \
                        , (newID, req['FIRST_NAME'], req['LAST_NAME'], req['GENDER'], req['BDATE'], req['ADDRESS'], facultyId))
        cnx.commit()

        resp = jsonify("added successful!")
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/test')
def test():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID FROM payment GROUP BY ID HAVING COUNT(*) = 8")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/allOld')
def allOld():
    try:
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID FROM student WHERE ID LIKE \"58%\"")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/show-non-graduated')
def showNonGraduated():
    try:
        listId = requests.get('http://127.0.0.1:5000/allOld')
        blackList = requests.get('http://127.0.0.1:5000/test')

        result = []
        for ele in listId.json():
            print(ele['ID'])
            for bkl in blackList.json():
                if ele['ID']==bkl['ID']:
                    result.append({"ID": ele['ID']})
                    break
        
        cnx = mysql.connect()
        cursor = cnx.cursor(pymysql.cursors.DictCursor)
        resp = jsonify(result)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cnx.close()