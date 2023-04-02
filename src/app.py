from flask import Flask, render_template
import db

app = Flask(__name__)


@app.route('/')
def index():
    active_populations = db.populations()
    overall_attendance = db.attendance()
    return render_template("index.html", active_populations=active_populations, overall_attendance=overall_attendance)


@app.route('/populations/<program>')
def populations(program):
    for_program = db.population_students(program)
    for_course = db.population_courses(program)
    abc = db.populations()
    return render_template("populations.html", program=for_program, abc=abc, for_course=for_course)


@app.route('/grades/<program>')
def grades(program):
    for_grade = db.students_grades(program)
    abc = db.populations()
    return render_template("grades.html", for_grade=for_grade, abc=abc)




if __name__=="__main__":
    app.run(debug=True)

db.close()