import json

class_dict = {}
for i in range(1000):
    with open(f"Git-Github/template/student-performance-template/students/{i}.json") as f:
        dict1 = json.load(f)
        class_dict[i] = dict1

# print(class_dict)
# print("\n\n")

def student_average_func(student):
    subjects = ["math", "science", "history", "english", "geography"]
    scores = [student[subject] for subject in subjects]
    average = sum(scores)/5

    return average

def subject_average(students):
    math = [subjects["math"] for subjects in students.values()]
    science = [subjects["math"] for subjects in students.values()]
    history = [subjects["history"] for subjects in students.values()]
    english = [subjects["english"] for subjects in students.values()]
    geography = [subjects["geography"] for subjects in students.values()]

    math_avg = sum(math)/len(math)
    science_avg = sum(science)/len(science)
    history_avg = sum(history)/len(history)
    english_avg = sum(english)/len(english)
    geography_avg = sum(geography)/len(geography)

    subject_averages = {
        "maths": math_avg,
        "science": science_avg,
        "history": history_avg,
        "english": english_avg,
        "geography": geography_avg
    }

    hardest = min([math_avg, science_avg, history_avg, geography_avg, english_avg])
    easiest = max([math_avg, science_avg, history_avg, geography_avg, english_avg])

    for key, value in subject_averages.items():
        if value == hardest:
            hardest_subject = key
        elif value == easiest:
            easiest_subject = key

    return [hardest_subject, easiest_subject]

def grade_average(students):
    grade1 = [student_average_func(student) for student in students.values() if student["grade"] == 1]
    grade2 = [student_average_func(student) for student in students.values() if student["grade"] == 2]
    grade3 = [student_average_func(student) for student in students.values() if student["grade"] == 3]
    grade4 = [student_average_func(student) for student in students.values() if student["grade"] == 4]
    grade5 = [student_average_func(student) for student in students.values() if student["grade"] == 5]
    grade6 = [student_average_func(student) for student in students.values() if student["grade"] == 6]
    grade7 = [student_average_func(student) for student in students.values() if student["grade"] == 7]
    grade8 = [student_average_func(student) for student in students.values() if student["grade"] == 8]

    grade1_avg = sum(grade1)/len(grade1)
    grade2_avg = sum(grade2)/len(grade1)
    grade3_avg = sum(grade3)/len(grade1)
    grade4_avg = sum(grade4)/len(grade1)
    grade5_avg = sum(grade5)/len(grade1)
    grade6_avg = sum(grade6)/len(grade1)
    grade7_avg = sum(grade7)/len(grade1)
    grade8_avg = sum(grade8)/len(grade1)

    grade_averages = {
        1: grade1_avg,
        2: grade2_avg,
        3: grade3_avg,
        4: grade4_avg,
        5: grade5_avg,
        6: grade6_avg,
        7: grade7_avg,
        8: grade8_avg,
    }

    worst = min([grade1_avg, grade2_avg, grade3_avg, grade4_avg, grade5_avg, grade6_avg, grade7_avg, grade8_avg,])
    best = max([grade1_avg, grade2_avg, grade3_avg, grade4_avg, grade5_avg, grade6_avg, grade7_avg, grade8_avg,])
    
    for key, value in grade_averages.items():
        if value == worst:
            worst_performing_grade = key
        elif value == best:
            best_performing_grade = key

    return [best_performing_grade, worst_performing_grade]
  
def best_worst_student(students):
    student_avg = [student_average_func(student) for student in students.values()]
    best_avg = max(student_avg)
    worst_avg = min(student_avg)

    for value, avg_score in zip(students.values(), student_avg):
        value["average score"] = avg_score

    for value in students.values():
        if value["average score"] == best_avg:
            best_student_id = value["id"]
        elif value["average score"] == worst_avg:
            worst_student_id = value["id"]

    return [best_student_id, worst_student_id]

def class_average(students):
    students_avg_score = [student_average_func(student) for student in students.values()]
    class_avg = sum(students_avg_score)/len(students_avg_score)

    return round(class_avg, 2)



print(f"Average Student Grade: {class_average(class_dict)}")
print(f"Hardest Subject: {subject_average(class_dict)[0]}")
print(f"Easiest Subject: {subject_average(class_dict)[1]}")
print(f"Best Performing Grade: {grade_average(class_dict)[0]}")
print(f"Worst Performing Grade: {grade_average(class_dict)[1]}")
print(f"Best Student ID: {best_worst_student(class_dict)[0]}")
print(f"Worst Student ID: {best_worst_student(class_dict)[1]}")