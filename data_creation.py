from datetime import *
import random
import pandas as pd

hours_range = (9, 14)
students_per_day = 20
total_students = 600
leaving_students = int(total_students * 0.75)


def create_datetime(hour, minutes):
    date_time_obj = datetime.strptime(f'{hour}:{minutes}:00', '%H:%M:%S')
    return date_time_obj.time()


def generate_students_by_day(current_students):
    student_per_day_std = 5
    random_students_num = students_per_day - student_per_day_std + random.randrange(student_per_day_std * 2)
    return min(current_students, random_students_num)


def generate_student_leaving_hour():
    hour = random.randrange(hours_range[0], hours_range[1])
    minute = random.randrange(0, 60)
    return create_datetime(hour, minute)


def generate_student_attempts():
    random_num = 0
    attempts_time = []
    while random_num < 1 / (len(attempts_time) + 2):
        attempts_time.append(5 + random.randrange(6))
        random_num = random.random()
    return attempts_time


def create_data():
    current_students = leaving_students
    df = pd.DataFrame(columns=['Day', 'Hour', 'Attempts', 'Checks_Lengths'])
    day_id = 1
    while current_students > 0:
        student_leaving_today = generate_students_by_day(current_students)
        for student in range(student_leaving_today):
            student_arrival_hour = generate_student_leaving_hour()
            checks_lengths = generate_student_attempts()
            if len(checks_lengths) <= 3:
                current_students -= 1
            df = df.append({'Day': day_id, 'Hour': student_arrival_hour, 'Attempts': len(checks_lengths),
                            'Checks_Lengths': checks_lengths}, ignore_index=True)
        day_id += 1
    df = df.sort_values(by=['Day', 'Hour']).reset_index(drop=True)
    return df
