import os
import jaydebeapi

#Connecting to Database via H2 console
def connect(db_driver_path, db_url, db_user, db_password):
    conn = jaydebeapi.connect('org.h2.Driver', db_url, [db_user, db_password], db_driver_path)
    return conn


PATH_TO_JAVA = r"C://Program Files//Java//jre1.8.0_361\bin"
H2_JAR = r"C://Users//alago//H2//bin//h2-2.1.214.jar"
URL = 'jdbc:h2:tcp://localhost/./test'
USER = 'sa'
PASSWORD = 'test'

os.environ["JAVA_HOME"] = PATH_TO_JAVA


connection = connect(H2_JAR, URL, USER, PASSWORD)
curs = connection.cursor()



def populations():
    curs.execute(
        """SELECT p.POPULATION_CODE, p.POPULATION_PERIOD, p.POPULATION_YEAR, count(s.STUDENT_EPITA_EMAIL)
            FROM POPULATIONS p
            JOIN STUDENTS s
            ON s.STUDENT_POPULATION_CODE_REF = p.POPULATION_CODE
            AND s.STUDENT_POPULATION_PERIOD_REF = p.POPULATION_PERIOD
            AND s.STUDENT_POPULATION_YEAR_REF = p.POPULATION_YEAR
            GROUP BY p.POPULATION_CODE, p.POPULATION_PERIOD, p.POPULATION_YEAR"""
    )
    active: list[tuple] = curs.fetchall()
    return active



def attendance():
    curs.execute(
        """SELECT STUDENT_POPULATION_CODE_REF, STUDENT_POPULATION_YEAR_REF, STUDENT_POPULATION_PERIOD_REF, SUM(a.ATTENDANCE_PRESENCE) *100/COUNT(ATTENDANCE_PRESENCE) FROM STUDENTS s  
            INNER JOIN ATTENDANCE a on STUDENT_EPITA_EMAIL = ATTENDANCE_STUDENT_REF
            WHERE STUDENT_POPULATION_YEAR_REF='2021'
            GROUP BY STUDENT_POPULATION_CODE_REF, STUDENT_POPULATION_PERIOD_REF,  s.STUDENT_POPULATION_YEAR_REF"""
    )
    o_attendance: list[tuple] = curs.fetchall()
    return o_attendance



def population_students(program):
    a  = """SELECT s.STUDENT_POPULATION_YEAR_REF, s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, COUNT(g.GRADE_COURSE_CODE_REF), s.STUDENT_POPULATION_CODE_REF 
            FROM CONTACTS c 
            JOIN STUDENTS s  ON s.STUDENT_CONTACT_REF = c.CONTACT_EMAIL 
            JOIN GRADES g ON g.GRADE_STUDENT_EPITA_EMAIL_REF = s.STUDENT_EPITA_EMAIL 
            WHERE g.GRADE_SCORE >= 10 
            AND s.STUDENT_POPULATION_CODE_REF = '{0}' 
            AND s.STUDENT_POPULATION_YEAR_REF = '2021'
            GROUP BY s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, s.STUDENT_POPULATION_YEAR_REF, s.STUDENT_POPULATION_CODE_REF;""".format(program)
    curs.execute(
        a
    )
    print(a)
    pop_student: list[tuple] = curs.fetchall()
    return pop_student


def population_courses(program):
    b  = """SELECT s.SESSION_POPULATION_YEAR, c.COURSE_CODE, c.COURSE_NAME, COUNT(s.SESSION_COURSE_REF),p.Program_assignment
            FROM COURSES c 
            JOIN SESSIONS s ON c.COURSE_CODE = s.SESSION_COURSE_REF
            JOIN PROGRAMS p ON c.COURSE_CODE = p.PROGRAM_COURSE_CODE_REF
            WHERE s.SESSION_POPULATION_YEAR = '2021' 
            AND p.PROGRAM_ASSIGNMENT = '{0}'
            GROUP BY c.COURSE_CODE, c.COURSE_NAME, p.PROGRAM_ASSIGNMENT, s.SESSION_POPULATION_YEAR;""".format(program)
    curs.execute(
        b
    )
    print(b)
    pop_course: list[tuple] = curs.fetchall()
    return pop_course


def students_grades(program):
    c = """SELECT STUDENT_POPULATION_YEAR_REF, s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, g.GRADE_COURSE_CODE_REF, AVG(g.GRADE_SCORE) AS COURSE_GRADE, s.STUDENT_POPULATION_CODE_REF
            FROM STUDENTS s 	
            INNER JOIN CONTACTS c ON s.STUDENT_CONTACT_REF = c.CONTACT_EMAIL AND s.STUDENT_POPULATION_CODE_REF = '{0}'
            INNER JOIN GRADES g ON s.STUDENT_EPITA_EMAIL = g.GRADE_STUDENT_EPITA_EMAIL_REF AND s.STUDENT_POPULATION_CODE_REF = '{0}' AND STUDENT_POPULATION_YEAR_REF ='2021'
            GROUP BY s.STUDENT_EPITA_EMAIL, g.GRADE_COURSE_CODE_REF;""".format(program)
    curs.execute(
        c
    )
    stud_grad: list[tuple] = curs.fetchall()
    return stud_grad



def close():
    connection.close()
    
