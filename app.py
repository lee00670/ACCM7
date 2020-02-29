from dominate.svg import switch
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired, Length

import inputCSV
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
Bootstrap(app)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jelee'
app.config['MYSQL_DB'] = 'accm'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET','POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        category = request.form['category']

        msg=category
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if(category=='professor'):
            cursor.execute('SELECT * FROM professor WHERE id = %s AND pw = %s', (username, password))
        elif (category=='coordinator'):
            cursor.execute('SELECT * FROM coordinator WHERE id = %s AND pw = %s', (username, password))
        elif (category=='secretary'):
            cursor.execute('SELECT * FROM secretary WHERE id = %s AND pw = %s', (username, password))
        elif (category=='student'):
            cursor.execute('SELECT * FROM student WHERE id = %s AND pw = %s', (username, password))

        bUpload ={0: 'hidden', 1: ''} [(category == 'coordinator')|(category == 'professor')]

        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['pw'] = account['pw']
            session['category'] = category
            session['bUpload'] = bUpload
            # Redirect to home page
            return render_template('home.html', bUpload=bUpload)

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('pw', None)
    session.pop('category', None)
    session.pop('bUpload', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET','POST'])
def register():
    print(url_for('register'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        category = request.form['category']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if (category == 'professor'):
            cursor.execute('SELECT * FROM professor WHERE id = %s AND pw = %s', (username, password))
        elif (category == 'coordinator'):
            cursor.execute('SELECT * FROM coordinator WHERE id = %s AND pw = %s', (username, password))
        elif (category == 'secretary'):
            cursor.execute('SELECT * FROM secretary WHERE id = %s AND pw = %s', (username, password))
        elif (category == 'student'):
            cursor.execute('SELECT * FROM student WHERE stduent_num = %s AND pw = %s', (username, password))

        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table

            cursor.execute('INSERT INTO user VALUES (%s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['id'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        category = session['category']
        if (category == 'professor'):
            cursor.execute('SELECT * FROM professor WHERE id = %s AND pw = %s', ([session['id']], [session['pw']]))
        elif (category == 'coordinator'):
            cursor.execute('SELECT * FROM coordinator WHERE id = %s AND pw = %s', ([session['id']], [session['pw']]))
        elif (category == 'secretary'):
            cursor.execute('SELECT * FROM secretary WHERE id = %s AND pw = %s',([session['id']], [session['pw']]))
        elif (category == 'student'):
            cursor.execute('SELECT * FROM student WHERE stduent_num = %s AND pw = %s', ([session['id']], [session['pw']]))

        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/input -
@app.route('/input')
def input():
    # upload csv file to mysql
    if 'loggedin' in session:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user WHERE id = %s', [session['username']])
        cursor.execute('SELECT * FROM user WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('input.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/uploadGrade
@app.route('/uploadGrade')
def uploadGrade():
    print("call uploadGrade")
    return render_template('uploadGrade.html', show=0)

# http://localhost:5000/uploadGrade2DB
@app.route('/uploadGrade2DB', methods=['POST'])
def uploadGrade2DB():
    print("call uploadGrade2DB")

    if request.method == 'POST' and 'pVersion' in request.form and 'cTerm' in request.form and 'sLevel' in request.form:
        print('call inputCSV2DB', request.form['pVersion'], request.form['cTerm'], request.form['sLevel'])
        print("call inputCSV2DB")
        inputCSV.inputCSV2DB(request.form['pVersion'], request.form['cTerm'], request.form['sLevel'])
        print("end inputCSV2DB")
    if 'loggedin' in session:
        # User is loggedin show them the home page
        print("call uploadGrade below")
        return render_template('uploadGrade.html', show=1, fileName=request.form['inputFile'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/viewGrade
@app.route('/viewGrade', methods=['GET','POST'])
def viewGrade():
    print("call viewGrade")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM user WHERE id = %s', [session['username']])
    cursor.execute('select distinct program_version  from program;')
    versionDict = cursor.fetchall()
    cursor.execute('SELECT program_version, pid, name FROM program ')
    programDict = cursor.fetchall()
    cursor.execute('select pid, coursemap.cid, title from coursemap inner join course using(cid) order by title;')
    courseDict = cursor.fetchall()

    if request.method == 'POST' and 'program' in request.form and 'level' in request.form and 'version' in request.form:
        if 'gid' in request.form and request.form['gid']:
            print(request.form['m_grade'])
            print(request.form['gid'])
            setQuery =''
            if 'm_grade' in request.form and request.form['gid']:
                setQuery = "letter_grade = '" + request.form['m_grade']+"', fcomment = '" + request.form['m_fcomment']+"', rcomment = '" + request.form['m_rcomment']+"'"

            query = "UPDATE grade SET "+setQuery+" WHERE gid='"+ request.form['gid']+"'"
            cursor.execute(query)
            mysql.connection.commit()

        if 'course' in request.form and request.form['course']:
            query = "select c.course_num, c.title, c.year from grade as g inner join student as s using(sid) inner join coursemap using(mapid) inner join program as p using(pid) inner join course as c using(cid) where p.pid = "+request.form['program'] +" and p.program_version='"+request.form['version'] +"' and s.level='"+request.form['level'] +"' and c.cid='"+request.form['course'] +"' group by c.course_num order by count(c.course_num) desc, course_num"
        else:
            query = "select c.course_num, c.title, c.year from grade as g inner join student as s using(sid) inner join coursemap using(mapid) inner join program as p using(pid) inner join course as c using(cid) where p.pid = "+request.form['program'] +" and p.program_version='"+request.form['version'] +"' and s.level='"+request.form['level'] +"' group by c.course_num order by count(c.course_num) desc, course_num"

        cursor.execute(query)
        clist = cursor.fetchall()

        query ="select p.name, p.program_version, gid, student_num, concat(s.fname, ' ' , s.lname) as fullname, s.level, fcomment,rcomment,  c.course_num, c.title, letter_grade, coursemap.level, p.pid, c.cid from grade as g inner join student as s using(sid) inner join coursemap using(mapid) inner join program as p using(pid) inner join course as c using(cid) where p.pid = "+request.form['program'] +" and p.program_version='"+request.form['version'] +"' and s.level='"+request.form['level'] +"' order by s.student_num, title"
        cursor.execute(query)
        result = cursor.fetchall()
        s = ''
        rDict=()
        d={}
        for r in result:
            if (s != r['student_num']):
                if (d):
                    rDict += (d,)

                d = {}
                s = r['student_num']
                d['student_num'] = s
                d['fullname'] = r['fullname']
                d['level'] = r['level']

            d[r['course_num']] = (r['letter_grade'])
            d[r['course_num']+ "_id"] = (r['gid'])

            comment = ''
            if (r['fcomment']):
                comment = "fcomment: " + r['fcomment']

            if (r['rcomment']):
                comment += " rcomment: " + r['rcomment']

            if (comment):
                d[r['course_num'] + "_c"] = comment
        if (d):
            rDict += (d,)

        if(len(rDict)):
            return render_template('viewGrade.html', vDict=versionDict, pDict=programDict, cDict=courseDict,
                                   values=request.form, rDict=rDict, clist=clist)
        else:
            return render_template('viewGrade.html', vDict=versionDict, pDict=programDict, cDict=courseDict,
                                   values=request.form, noData=True)


    return render_template('viewGrade.html', vDict=versionDict, pDict=programDict, cDict=courseDict, values=request.form)


