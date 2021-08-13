from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Lecture, Time, Department, CustomUser, Division
import pandas as pd
import numpy as np
from django.utils.text import slugify

import csv
fist = True

CSV_PATH = './data.csv'  # 3. csv 파일 경로
# Create your views here.
def set_lecture():
    with open(CSV_PATH, newline='', encoding="euc-kr") as csvfile:  # 4. newline =''
        data_reader = csv.DictReader(csvfile)
        print(data_reader)
        for row in data_reader:
            time = row['time']
            time = time.split(",")
            dayStart = ""
            dayEnd = ""
            print(row["division"])
            day = []
            try:
                for t in time:
                    dayStart = t[0:1] + t[1:3]
                    dayEnd = t[0:1] + t[5:7]
                    for i in range(int(dayStart[2:3]), int(dayEnd[2:3]) + 1):
                        day.append(dayStart[0] + str(i) + "a")
                        day.append(dayStart[0] + str(i) + "b")
                    if dayStart[3:4] == "b":
                        day.remove(dayStart[1:3] + "a")
                    if dayEnd[3:4] == "a":
                        day.remove(dayEnd[1:3] + "b")
            except:
                continue
            lecture = Lecture.objects.create(
                name = row['name'],
                code = row['code'],
                semester = int(row['semester'][0]),
                credit = row['credit'],
                grade = row['grade'],
            )
            # lecture.division = row['division'],
            # lecture.name = row['name'],
            # lecture.code = row['code'],
            # lecture.semester = int(row['semester']),
            # lecture.credit = row['credit'],
            # lecture.time = row['time'],
            # lecture.capacity = row['capacity'],
            # lecture.grade = row['grade']
            department, is_department = Department.objects.get_or_create(name=row['department'].strip())
            if is_department:
                department.slug = slugify(row["department"])
                department.save()
            lecture.department.add(department)
            try:
                for d in day:
                    print(d.lower())
                    time = Time.objects.get(slug=d.lower().strip())
                    lecture.time.add(time)
            except:
                continue
            division, is_division = Division.objects.get_or_create(name=row['division'])
            print(row["division"])
            if is_division:
                division.slug = slugify(row["division"])
                division.save()
            lecture.division = division
            lecture.save()



def main(request):
    return render(request, 'main.html')



def set_time_table():
    weeks = ['월', '화', '수', '목', '금']
    day_times = range(1, 10)
    day_parts = ['a', 'b']
    pk = 1
    for week in weeks:
        for day_time in day_times:
            for day_part in day_parts:
                slug = week + str(day_time) + day_part
                t = Time.objects.create(
                    week=week,
                    slug=slugify(slug, allow_unicode=True),
                    day = (str(day_time) + day_part)
                )
                t.save()
                print(t.slug)
                pk += 1


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


def get_rates_and_candidates(request):
    current_user = request.user
    lectures = current_user.lecture
    lecture_count = len(lectures)
    cr = np.random.normal(0, 4, size=lecture_count)
    candidates = []
    rates = []

    for i, lecture in enumerate(lectures.iterator()):
        candidates.append(
            int(cr[i] * lecture.current_user))
        rates.append(
            0 if cr[i] == 0 else 1 / cr[i]
        )

    return rates, candidates


def lander(request):
    context = dict()
    if request.user.is_authenticated:
        current_user = request.user
        # rates는 lecture에 대한 초당 클릭수 ( 1 / 경쟁률 )
        # candidates는 0, 4 사이의 정규분포
        rates, candidates = get_rates_and_candidates(request)
        context["rates"] = rates
        context["candidates"] = candidates

    return render(
        request,
        # url
        "stanbyPage",
        context
    )


def init():
    if fist:
        set_department()
        print("initalizing")
        try:
            pass
        except:
            pass
        try:
            set_time_table()
        except:
            pass
        set_lecture()
