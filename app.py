from flask import Flask, render_template, request, redirect, url_for
import time
import datetime

app = Flask(__name__)


student_list = {1: {'first_name': 'janet',
                    'last_name': 'ranada',
                    'created': '2020-01-10 13:12:33',
                    'last_updated': '2020-01-12 10:25:04',
                    'current_magic': ['Illusion 1', 'Possession 2', 'Invisibility 3', 'Invulnerability 4', 'Necromancer 5'],
                    'desired_magic': ['Immortality', 'Elemental'],
                    'desired_course': ['Alchemy advanced', 'Magic for day-to-day life'],
                    },
                2: {'first_name': 'igal',
                    'last_name': 'zeltser',
                    'created': '2019-11-10 03:12:33',
                    'last_updated': '2020-01-12 16:20:41',
                    'current_magic': ['Poison 5', 'Possession 4', 'Self-detonation 3', 'Summoning 2', 'Water breathing 1'],
                    'desired_magic': ['Invisibility', 'Healing'],
                    'desired_course': ['Alchemy advanced', 'Dating with magic'],
                    },
                3: {'first_name': 'nutz',
                    'last_name': 'kitten',
                    'created': '2020-01-09 23:01:15',
                    'last_updated': '2020-01-20 15:25:43',
                    'current_magic': ['Immortality 2', 'Invulnerability 2', 'Necromancer 2', 'Omnipresent 2', 'Omniscient 2'],
                    'desired_magic': ['Possession', 'Alchemy'],
                    'desired_course': ['Alchemy basics', 'Magic for day-to-day life'],
                    }
                }


magic = ['Alchemy', 'Animation', 'Conjuror', 'Disintegration', 'Elemental', 'Healing',
         'Illusion', 'Immortality', 'Invisibility', 'Invulnerability', 'Necromancer',
         'Omnipresent', 'Omniscient', 'Poison', 'Possession', 'Self-detonation',
         'Summoning', 'Water breathing']


def skills_list(status):
    levels = []
    for i in range(0, len(magic)):
        levels.append(request.form.get(status + ' ' + magic[i]))  

    skills = [magic[i] + " " + levels[i] for i in range(0,len(magic)) if levels[i] is not None]
    return skills


@app.route("/")
def landing_page():
    return render_template("landing_page.html")


@app.route("/home")
def home_page():
    return render_template("index.html")

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
    return render_template("view_student.html", info=student_list[int(record_id)], rec_id=record_id)


@app.route("/add", methods=['POST', 'GET'])
def add_student():
    message = request.args.get('msg')
    return render_template("add_student.html", message=message)


@app.route("/success", methods=['POST'])
def success_add():
    global student_list
    curr_time = time.time()
    creation_time = datetime.datetime.fromtimestamp(curr_time).strftime('%Y-%m-%d %H:%M:%S')
    new_key = max(student_list.keys()) + 1
    new_student = {}
    desired_magic_list = skills_list('Desired')
    current_magic_list = skills_list('Current')
    new_student['first_name'] = request.form["firstName"]
    new_student['last_name'] = request.form["lastName"]
    new_student['created'] = creation_time
    new_student['last_updated'] = creation_time
    new_student['current_magic'] = current_magic_list
    new_student['desired_magic'] = desired_magic_list
    new_student['desired_course'] = request.form.getlist('courseDesired')
    student_list[new_key] = new_student
    print('**********')  
    print('GET STATS') 
    all_list = []
    for student in student_list:
        the_list = [magic.split()[0] for magic in student_list[student]['current_magic']]
        print(student_list[student]['first_name'] + " " + student_list[student]['last_name'])
        print(the_list)
        all_list.append(the_list)
    flat_list = [item for sublist in all_list for item in sublist]
    curr_skill_counter = [flat_list.count(skill) for skill in magic]
    print('counter:', curr_skill_counter)
    print('possession>>', flat_list.count('Possession'))
    print('the GIANT flat list>>', flat_list)
    for i in range(0,len(magic)):
        print(magic[i], '=', curr_skill_counter[i])
        
    print("**********")    
    return render_template('add_student.html', message="Record successfully added.")
    # return redirect(url_for('view_student', record_id=new_key, info=student_list[new_key]))
    # return render_template("success.html", content=student_list[new_key], rec_id=new_key, heading='This record was successfully added:')


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(port=5005)
