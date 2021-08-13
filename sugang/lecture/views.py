from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Lecture, Time, Department, CustomUser
import pandas as pd
from django.utils.text import slugify


import csv

CSV_PATH = './data.csv'  # 3. csv 파일 경로
# Create your views here.
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


def set_time_table():
    weeks = ['월', '화', '수', '목', '금']
    day_times = range(1, 10)
    day_parts = ['A', 'B']
    pk = 1
    for week in weeks:
        for day_time in day_times:
            for day_part in day_parts:
                t = Time.objects.create()
                t.week = week
                t.day = (day_time + day_part)
                slug = week + day_time + day_part
                t.slug = slugify(slug, allow_unicode=True)
                t.save()
                pk += 1
    return redirect('/')


def set_department():
    departments = ["교양학부",
                   "기계공학부",
                   "디자인ㆍ건축공학부",
                   "메카트로닉스공학부",
                   "산업경영학부",
                   "에너지신소재화학공학부",
                   "융합학과",
                   "전기ㆍ전자ㆍ통신공학부",
                   "컴퓨터공학부",
                   "HRD학과"
                   ]
    for pk, d in enumerate(departments):
        department = Department.objects.create()
        department.name = d
        department.slug = slugify(pk)
        department.save()
 
def stanbyPage(request):

    return render(request, "stanbyPage") 

def countDown(request):

    return render(request, "countDown")


def set_users_timetable(request):
    user = request.user
    while user.credit > 18:
        lecture = Lecture.objects.filter(
            Q(max_user__gt=current_user) &
            Q(department__slug__exact=current_user.department)
        ).order_by("?")
        if user.credit + lecture.credit < 21:
            if not lecture in user.lecture:
                user.lecture.add(lecture)
                lecture.current_user += 1
    user.save()
