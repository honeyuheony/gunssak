from django.shortcuts import render
from django.db.models import Q
from lecture.models import *
import pandas as pd


# Create your views here.
def set_time_table():
    weeks = ['월', '화', '수', '목', '금']
    day_times = range(1, 9)
    day_parts = ['A', 'B']
    pk = 1
    for week in weeks:
        for day_time in day_tiems:
            for day_part in day_parts:
                t = Time.objects.create()
                t.week = week
                t.day = (day_time + day_part)
                t.slug = slugify(pk)
                t.save()
                pk += 1
    return redirect('/')



def set_department_table():
    department = ['메카트로닉스공학부', '교양학부', 'HRD학과', ]


def get_users_timetable(request):
    user = request.user
    while user.credit > 18:
        lecture = Lecture.objects.filter(
            Q(max_user__gt=current_user) &
            Q(department__slug__exact=user.department)
        ).order_by("?")
        if lecture.count() > 0:
            if user.credit + lecture.credit < 21:
                if not lecture in user.lecture:
                    user.lecture.add(lecture)
                    lecture.current_user += 1
        else:
            break
    user.save()
    return redirect('/')


def set_lecture_all_zero(request):
    lectures = Lecture.objects.iterator()
    for lecture in lectures:
        lecture.current_user = 0
        lecture.save()
    return redirect('/')

