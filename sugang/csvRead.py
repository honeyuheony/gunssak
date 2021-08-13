from lecture.models import *  # 2. App이름.models
import csv
import os
import django
import sys

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "sugang.settings")  # 1. 여기서 프로젝트명.settings입력
django.setup()

# 위의 과정까지가 python manage.py shell을 키는 것과 비슷한 효과


CSV_PATH = './data.csv'  # 3. csv 파일 경로

with open(CSV_PATH, newline='') as csvfile:  # 4. newline =''
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        time = row['time']
        time = time.split(",")
        week = ""
        day = []
        dayStart = ""
        dayEnd = ""
        for t in time:
            week = t[1:2]
            dayStart = t[2:5]
            dayEnd = t[6:9]
            for i in range(int(dayStart[1:3]), int(dayEnd[1:3] + 1)):
                day.append(i + "A")
                day.append(i + "B")
            if dayStart[3:4] == "B":
                day.remove(dayStart[1:3] + "A")
            if dayEnd[3:4] == "A":
                day.remove(dayEnd[1:3] + "B")
        Lecture.objects.create(
            name=row['name'],
            code=row['code'],
            semester=row['semester'],
            department=row['department'],
            division=row['division'],
            credit=row['credit'],
            time=row['time'],
            capacity=row['capacity'],
            grade=row['grade']

            # 6
        )
