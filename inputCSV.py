import csv
import mysql.connector

def inputCSV2DB(pVersion, sLevel):
   print("call uploadGrade2DB in inputCSV", pVersion, sLevel)
   mydb = mysql.connector.connect(host='localhost', user='root', password='jelee', database='accm')
   print("database connected")

   cursor = mydb.cursor()
   csv_data = csv.reader(open('./static/input.csv', encoding='UTF-8-sig'))
   for row in csv_data:
      print(row)
      insertQuery = "INSERT INTO ac_grade_input(program_version, course_year, student_level, "+\
                    "term, program_code, program_name, course_level, student_num, student_fname, student_lname, student_email, prof_fname, prof_lname, course_num, course_title, "+\
                    "letter_grade, percent, fcomment, rcomment) VALUES('"+pVersion+"', '', '"+sLevel+"',"
      cursor.execute(insertQuery+"%s, %s, %s, %s, %s, %s, %s, '', %s, %s, %s, %s, %s, %s, %s, %s)", row)

   print("insert program")
   #insert program
   cursor.execute('INSERT INTO program(code, name, program_version) SELECT distinct(program_code), program_name, program_version FROM ac_grade_input as a '+
                   'WHERE NOT EXISTS (SELECT * FROM program WHERE code=a.program_code AND program_version = a.program_version)')

   print("insert course")
   #insert course
   cursor.execute('INSERT INTO course(course_num, title, year) SELECT distinct(course_num), course_title, course_year FROM ac_grade_input as a '+
                  'WHERE NOT EXISTS (SELECT * FROM course WHERE course_num=a.course_num AND year=a.course_year)')

   print("insert coursemap")
   #insert coursemap
   cursor.execute('insert into coursemap(pid, cid, level, term) '+
                  'select program.pid, course.cid, a.course_level, a.term '+
                  'from ac_grade_input as a '+
                  'inner join program '+
                  'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'inner join course '+
                  'on (course.course_num = a.course_num and course.year = a.course_year) '+
                  'where not exists(select * from coursemap '+
                  'where pid = program.pid and cid = course.cid and course_level=a.course_level and term = a.term) '+
                  'group by program.pid, course.cid')

   print("insert student")
   #insert student
   cursor.execute('insert into student (student_num, fname, lname, level, email) '+
                  'select distinct(student_num), student_fname, student_lname, student_level, student_email '+
                  'from ac_grade_input as a '+
                  'where not exists(select * from student '+
                  'where student_num=a.student_num)')

   print("insert enrollment")
   #insert enrollment
   cursor.execute('insert into enrollment(sid, pid) '+
                  'select student.sid, program.pid '+
                  'from ac_grade_input as a '+
                  'inner join student '+
                     'on(student.student_num = a.student_num and student.level = a.student_level) '+
                  'inner join program '+
                     'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'where not exists(select * from enrollment '+
                     'where sid = student.sid and pid = program.pid) '+
                  'group by student.sid, program.pid')

   print("insert professor")
   #insert professor
   cursor.execute('insert into professor(fname, lname) '+
                  'select distinct(prof_fname), prof_lname '+
                  'from ac_grade_input as a '+
                  'where not exists(select * from professor '+
                  'where UPPER(fname)  = UPPER(a.prof_fname) and UPPER(lname) = UPPER(a.prof_lname));')

   print("insert teach")
   #insert teach
   cursor.execute('insert into teach(profid, mapid) '+
                  'select professor.profid, coursemap.mapid '+
                  'from ac_grade_input as a '+
                  'inner join professor '+
                  'on(UPPER(professor.fname) = UPPER(a.prof_fname) and UPPER(professor.lname) = UPPER(a.prof_lname)) '+
                  'inner join program '+
                  'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'inner join course '+
                  'on (course.course_num = a.course_num and course.year = a.course_year) '+
                  'inner join coursemap '+
                  'on(coursemap.pid = program.pid and coursemap.cid=course.cid) '+
                  'where not exists(select * from teach '+
                  'where profid = professor.profid and mapid = coursemap.mapid) '+
                  'group by professor.profid, coursemap.mapid;')

   print("insert grade")
   #insert grade
   cursor.execute('insert into grade(sid, mapid, letter_grade, percent, fcomment, rcomment) '+
                  'select student.sid, coursemap.mapid, a.letter_grade, a.percent, a.fcomment, a.rcomment '+
                  'from ac_grade_input as a '+
                  'inner join student '+
                  'on(student.student_num = a.student_num and student.level = a.student_level) '+
                  'inner join program '+
                  'on(program.code = a.program_code and program.program_version = a.program_version) '+
                  'inner join course '+
                  'on (course.course_num = a.course_num and course.year = a.course_year) '+
                  'inner join coursemap '+
                  'on(coursemap.pid = program.pid and coursemap.cid=course.cid) '+
                  'where not exists(select * from grade '+
                  'where sid = student.sid and mapid = coursemap.mapid) '+
                  'group by student.sid, coursemap.mapid;')

   print("insertion done.")

   print("delete ac_grade_input")
   #insert grade
   cursor.execute('delete from ac_grade_input')



   mydb.commit()
   cursor.close()

   print("DONE")

