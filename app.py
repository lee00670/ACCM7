import os
import re

import MySQLdb.cursors
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt

import inputCSV

app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = 'd:/1.MyDoc/2020W/CST8268_Project/project/ACCM7/Upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'accm'
app.config.from_pyfile('./static/config.cfg')

# app.config['MAIL_SERVER'] = "localhost"
# app.config['MAIL_PORT'] = 8025
# python -m smtpd -n -c DebuggingServer localhost:8025 ==> for emulated email server

#mgail setting
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = 1
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
        passwordUser = request.form['password']
        category = request.form['category']

        msg=category
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # if(category=='professor'):
        #     cursor.execute('SELECT * FROM professor WHERE id = %s AND pw = %s', (username, password))
        # elif (category=='coordinator'):
        #     cursor.execute('SELECT * FROM coordinator WHERE id = %s AND pw = %s', (username, password))
        # elif (category=='secretary'):
        #     cursor.execute('SELECT * FROM secretary WHERE id = %s AND pw = %s', (username, password))
        # elif (category=='student'):
        #     cursor.execute('SELECT student_num as id, pw FROM student WHERE student_num = %s AND pw = %s', (username, password))
        result = 0
        if (category == 'professor'):
            result = cursor.execute('SELECT * FROM professor WHERE id = %s',[username])
        elif (category == 'coordinator'):
            result = cursor.execute('SELECT * FROM coordinator WHERE id = %s',[username])
        elif (category == 'secretary'):
            result = cursor.execute('SELECT * FROM secretary WHERE id = %s', [username])
        elif (category == 'student'):
            result = cursor.execute('SELECT student_num as id, pw, sid FROM student WHERE student_num = %s', [username])

        bUpload ={0: 'hidden', 1: ''} [(category == 'coordinator')|(category == 'secretary')]

        if result > 0:
            # Fetch one record and return result
            account = cursor.fetchone()
            password = account['pw']

            if sha256_crypt.verify(passwordUser, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['pw'] = account['pw']
                session['category'] = category
                session['bUpload'] = bUpload
                session['revision'] = 1
                if(category == 'student'):
                    session['sid'] = account['sid']
                
                # Redirect to home page
                return render_template('home.html', bUpload=bUpload)
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password'

        cursor.close()

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
    session.pop('revision', None)
    session.pop('sid', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET','POST'])
def register():
    print(url_for('register'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'category' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        password = sha256_crypt.hash(password)

        email = request.form['email']
        category = request.form['category']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if (category == 'professor'):
            cursor.execute('SELECT * FROM professor WHERE id = "'+username+'"')
        elif (category == 'coordinator'):
            cursor.execute('SELECT * FROM coordinator WHERE id = "'+username+'"')
        elif (category == 'secretary'):
            cursor.execute('SELECT * FROM secretary WHERE id = "'+username+'"')
        elif (category == 'student'):
            cursor.execute('SELECT * FROM student WHERE student_num = "'+username+'"')

        account = cursor.fetchone()
        cursor.close()
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

            # mail = Mail(app)
            # msg = Message('New request for the registration of ACCM', sender="jelee1003@gmail.com", recipients=['jelee1003@gmail.com'])
            # # msg = Message('test subject', sender='algonquinlive.com\lee00670', recipients=['jelee1003@gmail.com'])
            # msg.html="<h3>The new resistration is requested as below.</h3>username: "+username+"<br>password: "+password+"<br>email: "+email+"<br>Category: "+category
            # mail.send(msg)

            msg = ''
            success = "s"
            return render_template('register.html', msg=msg, success=success)
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
        return render_template('home.html', bUpload=session['bUpload'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile', methods=['POST','GET'])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        category = session['category']
        if (category == 'professor'):
            cursor.execute('select distinct id, fname, lname, email, pw, name from professor inner join teach using(profid) inner join coursemap using(mapid) inner join program using(pid) where id=%s and pw=%s', ([session['id']], [session['pw']]))
        elif (category == 'coordinator'):
            cursor.execute('SELECT * FROM coordinator inner join program using(pid) WHERE id = %s AND pw = %s', ([session['id']], [session['pw']]))
        elif (category == 'secretary'):
            cursor.execute('select id, fname, lname, pw, email, name from secretary inner join program_secretary using (secid) inner join program using(pid) where id=%s and pw=%s',([session['id']], [session['pw']]))
        elif (category == 'student'):
            cursor.execute('select student_num as id, fname, lname, pw, email, name from student inner join enrollment using (sid) inner join  program using (pid) where student_num=%s and pw=%s', ([session['id']], [session['pw']]))

        account = cursor.fetchone()

        if request.method == 'POST' and 'password' in request.form:

            #if password is right, show the profile info
            if(sha256_crypt.verify(request.form['password'], session['pw'])):
            # if(session['pw'] == request.form['password']):
                return render_template('profile.html', account=account, category=session['category'], msg="s")
            else:
                return render_template('profile.html', account=account, category=session['category'], msg="The password is wrong.")
        # if user requests to change password
        elif request.method == 'POST' and 'newPassword' in request.form and 'newPassword2' in request.form:
            if(request.form['newPassword'] == request.form['newPassword2']):
                try:
                    category = session['category']
                    #make hash using new password user inputs
                    pw = sha256_crypt.hash(request.form['newPassword'])

                    #update password
                    if (category == 'professor'):
                        cursor.execute('update professor set pw = %s WHERE id = %s',
                                       (pw, [session['id']]))
                    elif (category == 'coordinator'):
                        cursor.execute(' update coordinator set pw = %s where id= %s',
                                       (pw, [session['id']]))
                    elif (category == 'secretary'):
                        cursor.execute('update secretary set pw = %s WHERE id = %s',
                                       (pw, [session['id']]))
                    elif (category == 'student'):
                        cursor.execute('update student set pw = %s WHERE student_num = %s',
                                       (pw, [session['id']]))
                    mysql.connection.commit()
                    cursor.close()
                    #save new hash to session
                    session['pw'] = pw
                    return render_template('profile.html', account=account, category=session['category'], msg="New password is updated.")
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print(e)
                    cursor.close()
                    return render_template('profile.html', account=account, category=session['category'], msg="New password is not changed.")
            else:
                cursor.close()
                return render_template('profile.html', account=account, category=session['category'],
                                       msg="New password is not changed.")
        cursor.close()
        return render_template('profile.html', account=account, category=session['category'])
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

    # if request.method == 'POST' and 'pVersion' in request.form and 'cTerm' in request.form and 'sLevel' in request.form:
    if request.method == 'POST' and 'pVersion' in request.form and 'cTerm' in request.form:
        print("call inputCSV2DB")
        file = request.files['inputFile']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        #call inputCSV2DB with file name
        inputCSV.inputCSV2DB(request.form['pVersion'], request.form['cTerm'], "", file.filename)

    if 'loggedin' in session:
        # User is loggedin show them the home page
        print("call uploadGrade below")
        return render_template('uploadGrade.html', show=1, fileName=file.filename)

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/viewGrade
@app.route('/viewGrade', methods=['GET','POST'])
def viewGrade():
    if(session['category'] == 'student'):
        return viewFlowchart(str(session['sid']), '','','','')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM user WHERE id = %s', [session['username']])
    cursor.execute('select distinct program_version  from program;')
    versionDict = cursor.fetchall()
    cursor.execute('SELECT program_version, pid, name FROM program ')
    programDict = cursor.fetchall()
    cursor.execute('select distinct level, pid from coursemap order by level')
    lvlDict = cursor.fetchall()
    cursor.execute('select pid, coursemap.cid, title, level from coursemap inner join course using(cid) order by title;')
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
        elif 'gid' in request.form and request.form['m_grade']:
            valuesQuery= "values('" + request.form['sid']+"', '" + request.form['mapid']+"', '" + request.form['m_grade']+"', '" + request.form['m_fcomment']+"', '" + request.form['m_rcomment']+"')"
            query = "INSERT INTO grade(sid, mapid, letter_grade, fcomment, rcomment) " + valuesQuery
            cursor.execute(query)
            mysql.connection.commit()

        if 'delete_gid' in request.form and request.form['delete_gid']:
            query = "delete from grade where gid ='"+request.form['delete_gid']+"'"
            cursor.execute(query)
            mysql.connection.commit()

        if 'course' in request.form and request.form['course'] and request.form['course'] != 'null':
            query = "select c.course_num, c.title, coursemap.level, coursemap.mapid from grade as g inner join student as s using(sid) inner join coursemap using(mapid) inner join program as p using(pid) inner join course as c using(cid) where p.pid = "+request.form['program'] +" and p.program_version='"+request.form['version'] +"' and coursemap.level='"+request.form['level'] +"' and c.cid='"+request.form['course'] +"' group by c.course_num order by course_num"
        else:
            query = "select c.course_num, c.title, coursemap.level, coursemap.mapid from grade as g inner join student as s using(sid) inner join coursemap using(mapid) inner join program as p using(pid) inner join course as c using(cid) where p.pid = "+request.form['program'] +" and p.program_version='"+request.form['version'] +"' and coursemap.level='"+request.form['level'] +"' group by c.course_num order by course_num"

        cursor.execute(query)
        #get the course list as program, version and level
        clist = cursor.fetchall()

        #get all the grade for every students with program, version and level
        query ="select p.name, p.program_version, gid, student_num, sid, concat(s.fname, ' ' , s.lname) as fullname, s.level, fcomment,rcomment,  c.course_num, c.title, letter_grade, coursemap.level, p.pid, c.cid from grade as g inner join student as s using(sid) inner join coursemap using(mapid) inner join program as p using(pid) inner join course as c using(cid) where p.pid = "+request.form['program'] +" and p.program_version='"+request.form['version'] +"' and coursemap.level='"+request.form['level'] +"' order by s.student_num, title"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        s = ''
        rDict=()
        d={}
        #save grade info for each student to dictionary
        for r in result:
            if (s != r['student_num']):
                if (d):
                    rDict += (d,)

                d = {}
                s = r['student_num']
                d['student_num'] = s
                d['sid'] = r['sid']
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

        if (session['category'] != 'coordinator' and session['category'] != 'secretary' ):
            edit='disabled'
        else:
            edit = ''
        #call viewGrade.html with result
        if(len(rDict)):
            return render_template('viewGrade.html', vDict=versionDict, pDict=programDict, lvlDict=lvlDict, cDict=courseDict,
                                   values=request.form, rDict=rDict, clist=clist, edit=edit)
        else:
            return render_template('viewGrade.html', vDict=versionDict, pDict=programDict, lvlDict=lvlDict, cDict=courseDict,
                                   values=request.form, noData=True)


    return render_template('viewGrade.html', vDict=versionDict, pDict=programDict, lvlDict=lvlDict, cDict=courseDict, values=request.form)




# http://localhost:5000/viewFlowchart

@app.route('/viewFlowchart/<string:sid>/<string:sVersion>/<string:sProgram>/<string:sLevel>/<string:sCourse>', methods=['GET','POST'])
def viewFlowchart(sid, sVersion, sProgram, sLevel, sCourse):
    # print("call viewFlowchart", sid, sVersion, sProgram, sLevel, sCourse)
    # print("call viewFlowchart", session['category'])

    # get coordinator and secretary session
    if session['category'] is 'coordinator' or 'secretary':
        admin_session = True
    else:
        admin_session = False


    revision = session['revision']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # retrieve grade input and update student's grade for that course
    if request.method == 'POST':
        new_grade = request.form['inputGradeFlowchart']
        # get hidden grade id
        grade_id = request.values.get('gradeID')
        # get hidden mapid
        get_mapid = request.values.get('mapid')
        print("call viewFlowchart", new_grade)
        print("call viewFlowchart", grade_id)
        print("call viewFlowchart", get_mapid)

        cursor.execute("update grade " +
                       "SET letter_grade= '" + new_grade + "' " +
                       "where gid=" + grade_id)
        mysql.connection.commit()



    # get flowchart basic layout
    cursor.execute("SELECT flowchart.sequence, coursemap.mapid, course.course_num, course.title " +
                   "FROM flowchart " +
                   "INNER JOIN coursemap USING(mapid) " +
                   "INNER JOIN course USING(cid) " +
                   "ORDER BY flowchart.sequence ASC")
    flowchart = cursor.fetchall()

    # flowchart layout list
    flowchart_courses = []

    mainc = []
    for c in flowchart:
        flowchart_courses.append({'id': c['sequence'], 'mapid': c['mapid'], 'ccode': c['course_num'], 'title': c['title']})
        mainc.append(c['course_num'])



    # get courses that have a prerequisite
    pre_courses = []
    for course in flowchart_courses:
        # pre_course.append(course['course_num'])
        cursor.execute(
            "SELECT distinct flowchart.sequence, course.course_num, course.title, prerequisite.mapid, prerequisite.prerequisite " +
            "FROM prerequisite " +
            "INNER JOIN coursemap USING (mapid) " +
            "INNER JOIN course USING (cid) " +
            "INNER JOIN flowchart USING (mapid) " +
            "WHERE course.course_num = '" + course['ccode'] + "' " +
            "ORDER BY flowchart.sequence ASC;")

        prereq_results = cursor.fetchall()

        # pre_course.append(prereqs)
        for c in prereq_results:
            pre_courses.append(
                {'sequence': c['sequence'], 'ccode': c['course_num'], 'title': c['title'], 'c_mapid': c['mapid'],
                 'c_prereq': c['prerequisite']})

    # get courses that are prerequisites
    items_c = []
    for d in pre_courses:
        cursor.execute(
            "SELECT distinct flowchart.sequence, course.course_num, course.title, coursemap.mapid as 'prereq_id' " +
            "FROM course " +
            "INNER JOIN coursemap USING (cid) " +
            "INNER JOIN flowchart USING (mapid) " +
            "where coursemap.mapid = " + str(d['c_prereq']) + " " +
            "ORDER BY flowchart.sequence ASC;")
        pre_c = cursor.fetchall()
        for c in pre_c:
            items_c.append({'sequence': c['sequence'], 'ccode': c['course_num'], 'title': c['title'],
                            'pre_id': c['prereq_id']})

    # links between prerequisite courses: sources and targets
    links = []
    for i in range(len(pre_courses)):
        if pre_courses[i]['c_prereq'] == items_c[i]['pre_id']:
            links.append({'source_id': items_c[i]['sequence'], 'source': items_c[i]['ccode'],
                          'target_id': pre_courses[i]['sequence'], 'target': pre_courses[i]['ccode']})
    # remove duplicates
    seen = set()

    #final prereq list
    prereq_links = []
    for duplicates in links:
        t = tuple(duplicates.items())
        if t not in seen:
            seen.add(t)
            prereq_links.append(duplicates)



    # get student courses
    cursor.execute(
            "select distinct flowchart.sequence, concat(professor.fname, ' ' , professor.lname) as 'Professor Name', course.course_num, course.title, " +
            "term, concat(student.fname, ' ', student.lname) as 'Student Name', student.student_num, letter_grade, coursemap.mapid, gid, " +
            "fcomment, rcomment " +
            "from grade " +
            "inner join coursemap using(mapid) inner join course using (cid) inner join teach using(mapid) " +
            "inner join professor using(profid) inner join student using (sid) " +
            "left join flowchart on flowchart.mapid = coursemap.mapid "
            "where sid=" + sid + " " +
            "GROUP BY course.course_num " +
            "order by flowchart.sequence ASC")
    results = cursor.fetchall()

    student_name = ''
    student_num = ''

    # student results
    student_grades = []
    for r in results:
        student_name = r['Student Name']
        student_num = r['student_num']
        student_grades.append({'id': r['sequence'], 'student_name': r['Student Name'], 'student_num': r['student_num'],
                              'ccode': r['course_num'], 'coursename': r['title'], 'term': r['term'], 'prof': r['Professor Name'],
                               'grade': r['letter_grade'], 'mapid': r['mapid'], 'gid': r['gid'], 'fcomment': r['fcomment'], 'rcomment': r['rcomment']})


    revision += 1
    # session['revision'] = revision

    r = revision
    bBackKey = not (session['category'] == 'student')
    bEditGrade = (session['category'] == 'coordinator' or session['category'] == 'secretary')
    v = {'version': sVersion, 'program': sProgram, 'level':sLevel, 'course': sCourse}

    return render_template('viewFlowchart.html', flowchart_courses=flowchart_courses, prerequisite_links=prereq_links, sid = sid,
                           student_results = student_grades, studentName = student_name, studentNum = student_num, values=request.form,
                           bBackKey=bBackKey, random=r, admin_session = admin_session, v=v, bEditGrade=bEditGrade)

