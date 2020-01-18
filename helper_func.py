from flask import request
import time
import datetime
from crm_data import student_list, magic, courses, houses


def skills_list(status):
    levels = []
    for i in range(0, len(magic)):
        levels.append(request.form.get(status + ' ' + magic[i]))

    skills = [magic[i] + " " + levels[i]
              for i in range(0, len(magic)) if levels[i] is not '0']
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


def get_crm_time_year(_target_timestamp):
    global student_list
    unixtime_list = [student_list[key][_target_timestamp] for key in student_list]
    datetime_yr = [int(datetime.datetime.fromtimestamp(
        unixtime).strftime('%Y')) for unixtime in unixtime_list]
    year_unique = sorted(set(datetime_yr))
    year_counter = [datetime_yr.count(year) for year in year_unique]
    return year_unique, year_counter


def convert_time(_label):
    global student_list
    unixtime_list = [student_list[student][_label] for student in student_list]
    datetime_list = [datetime.datetime.fromtimestamp(unixtime).strftime(
        '%Y-%m-%d %H:%M:%S') for unixtime in unixtime_list]
    student_key = [key for key in student_list]
    datetime_dict = {}

    for i in range(0, len(datetime_list)):
        datetime_dict[student_key[i]] = datetime_list[i]

    return datetime_dict
