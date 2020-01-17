from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import datetime
from crm_data import student_list, magic, courses, houses

app = Flask(__name__)


def skills_list(status):
    levels = []
    for i in range(0, len(magic)):
        levels.append(request.form.get(status + ' ' + magic[i]))

    skills = [magic[i] + " " + levels[i]
              for i in range(0, len(magic)) if levels[i] is not None]
    return skills


def get_crm_skills_record(_target_magic):
    global student_list
    global magic
    all_magic = []
    for student in student_list:
        student_magic_list = [magic.split()[0]
                              for magic in student_list[student][_target_magic]]
        all_magic.append(student_magic_list)

    flatlist_magic = [item for sublist in all_magic for item in sublist]
    skill_counter = [flatlist_magic.count(skill) for skill in magic]
    return skill_counter


@app.route("/")
def landing_page():
    return render_template("landing_page.html")


@app.route("/get_data")
def get_data():
    data_to_pass = {}
    current_skill_counter = get_crm_skills_record("current_magic")
    desired_skill_counter = get_crm_skills_record("desired_magic")
    data_to_pass["current_magic_counter"] = current_skill_counter
    data_to_pass["desired_magic_counter"] = desired_skill_counter
    data_to_pass["magic_name"] = magic
    return jsonify(data_to_pass)


@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/dashboard")
def show_dashboard():
    return render_template("dashboard.html")


@app.route("/students")
def list_students():
    return render_template("students.html", text=student_list)


@app.route("/find")
def find_student():
    return render_template("find_student.html")


@app.route("/student/<string:record_id>")
def view_student(record_id):
    return render_template("view_student.html",
                           info=student_list[int(record_id)],
                           rec_id=record_id)


@app.route("/student/<string:record_id>/update", methods=['GET', 'POST'])
def update_student(record_id):
    global student_list
    if request.method == 'GET':
        return render_template('update_student.html',
                               student_data=student_list[int(record_id)],
                               all_magic=magic,
                               all_courses=courses,
                               rec_id=record_id)
    else:  # method is POST
        curr_time = time.time()
        update_time = datetime.datetime.fromtimestamp(
            curr_time).strftime('%Y-%m-%d %H:%M:%S')
        desired_magic_list = skills_list('Desired')
        all_current_magic = skills_list('Current')
        student_list[int(record_id)]['first_name'] = request.form["firstName"]
        student_list[int(record_id)]['last_name'] = request.form["lastName"]
        student_list[int(record_id)]['last_updated'] = update_time
        student_list[int(record_id)]['current_magic'] = all_current_magic
        student_list[int(record_id)]['desired_magic'] = desired_magic_list
        student_list[int(record_id)]['desired_course'] = request.form.getlist(
            'courseDesired')
        return render_template('update_student.html',
                               student_data=student_list[int(record_id)],
                               all_magic=magic,
                               all_courses=courses,
                               rec_id=record_id,
                               message='Record Updated')


@app.route("/add", methods=['POST', 'GET'])
def add_student():
    message = request.args.get('msg')
    return render_template("add_student.html",
                           message=message,
                           all_magic=magic,
                           all_courses=courses)


@app.route("/student/<string:record_id>/delete")
def delete_student(record_id):
    print(student_list[int(record_id)])
    del student_list[int(record_id)]
    return redirect("/students")


@app.route("/success", methods=['POST'])
def success_add():
    global student_list
    curr_time = time.time()
    creation_time = datetime.datetime.fromtimestamp(
        curr_time).strftime('%Y-%m-%d %H:%M:%S')
    new_key = max(student_list.keys()) + 1
    new_student = {}
    desired_magic_list = skills_list('Desired')
    all_current_magic = skills_list('Current')
    new_student['first_name'] = request.form["firstName"]
    new_student['last_name'] = request.form["lastName"]
    new_student['created'] = creation_time
    new_student['last_updated'] = creation_time
    new_student['current_magic'] = all_current_magic
    new_student['desired_magic'] = desired_magic_list
    new_student['desired_course'] = request.form.getlist('courseDesired')
    student_list[new_key] = new_student
    return render_template('add_student.html', message="Record successfully added.")
    

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(port=5005)
