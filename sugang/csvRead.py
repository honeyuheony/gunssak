from lecture.models import *
import csv
import os
import django
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sugang.settings")
django.setup()
# 현재 디렉토리 경로 표시


# 프로젝트명.settings


CSV_PATH = './data.csv'  # 3. csv 파일 경로

with open(CSV_PATH, newline='') as csvfile:  # 4. newline =''
    data_reader = csv.DictReader(csvfile)
    day = []
    for row in data_reader:
        time = row['time']
        time = time.split(",")
        dayStart = ""
        dayEnd = ""
        for t in time:
            dayStart = t[0:1] + t[1:3]
            dayEnd = t[0:1] + t[5:7]
            for i in range(int(dayStart[1:3]), int(dayEnd[1:3] + 1)):
                day.append(i + "A")
                day.append(i + "B")
            if dayStart[3:4] == "B":
                day.remove(dayStart[1:3] + "A")
            if dayEnd[3:4] == "A":
                day.remove(dayEnd[1:3] + "B")
        lecture = Lecture.objects.create(
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

        for d in day:
            time = Time.objects.get(slug=d)
            lecture.time.add(time)
