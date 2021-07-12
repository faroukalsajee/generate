import warnings

import pandas as pd
import sys, os, warnings, json

warnings.filterwarnings('ignore')
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# courses = pd.read_csv("Resources/courses.csv")
# marks = pd.read_csv("Resources/marks.csv")
# students = pd.read_csv("Resources/students.csv")
# tests = pd.read_csv("Resources/tests.csv")
# print(sys.argv)
[script_name, courses_path, students_path, tests_path, marks_path, output_path] = sys.argv
courses = pd.read_csv(courses_path)
marks = pd.read_csv(marks_path)
students = pd.read_csv(students_path)
tests = pd.read_csv(tests_path)


# -----------------------------------------------------------------
# -----------------------------------------------------------------
def get_info(student_data):
    student_data["course_id"] = 0
    student_data["test_weight"] = 0.0
    student_data["course_name"] = ""
    student_data["teacher"] = ""
    student_data["average_Course"] = 0.0
    student_data["average"] = 0.0
    for j in range(student_data.shape[0]):
        t_id = student_data["test_id"][j]
        student_data["course_id"][j] = int(tests.query('id == @t_id').reset_index(drop=True)["course_id"][0])
        student_data["test_weight"][j] = round(tests.query('id == @t_id').reset_index(drop=True)["weight"][0], 2)
        student_data["course_name"][j] = \
            courses[courses["id"] == student_data["course_id"][j]].reset_index(drop=True)["name"][0]
        student_data["teacher"][j] = \
            courses[courses["id"] == student_data["course_id"][j]].reset_index(drop=True)["teacher"][0]
    for j in range(student_data.shape[0]):
        c_id = student_data["course_id"][j]
        tmp = student_data.query('course_id == @c_id')
        student_data["average_Course"][j] = round((tmp["mark"] * tmp["test_weight"] / tmp["test_weight"].sum()).sum(),
                                                  2)
    tmp = student_data.groupby(by="course_name")
    student_data["average"] = round(tmp.average_Course.mean().mean(), 2)
    return student_data


# -----------------------------------------------------------------
# -----------------------------------------------------------------
def main():
    students_list = []
    students_list_pandas = []
    tests.groupby("course_id").sum()
    check_list = tests.groupby("course_id").sum().shape[0] * [100]
    cond = list(tests.groupby("course_id").sum()["weight"]) == check_list
    if cond:
        for i in range(students.shape[0]):
            student = dict()
            student["id"] = int(students["id"][i])
            student["name"] = students["name"][i]
            for j in range(marks.shape[0]):
                s_id = student["id"]
                student_data = marks.query('student_id == @s_id').reset_index(drop=True)
                student_data = get_info(student_data)
                student["totalAverage"] = float(student_data["average"][0])
                courses_name = list(student_data["course_name"].unique())
                courses_list = []
                for c_name in courses_name:
                    courses_ = dict()
                    courses_data = student_data[student_data["course_name"] == c_name].reset_index(drop=True)
                    courses_["id"] = int(courses_data["course_id"][0])
                    courses_["name"] = courses_data["course_name"][0]
                    courses_["teacher"] = courses_data["teacher"][0]
                    courses_["courseAverage"] = round(courses_data["average_Course"][0], 2)
                    courses_list.append(courses_)
                student["courses"] = courses_list
            students_list_pandas.append(student_data)
            students_list.append(student)
        studenst_data = dict()
        studenst_data["students"] = students_list
    else:
        studenst_data = {"error": "Invalid course weights"}
    with open(output_path, 'w') as f:
        json.dump(studenst_data, f, indent=1)


# -----------------------------------------------------------------
# -----------------------------------------------------------------
if __name__ == "__main__":
    main()
