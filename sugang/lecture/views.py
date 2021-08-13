from django.shortcuts import render
from django.db.models import Q
from lecture.models import *
import pandas as pd

# Create your views here.
def set_time_table():
    weeks = ['mon', 'tue', 'wen', 'thu', 'fri']
    for i, week in enumerate(weeks):
        for j in range(0, 18):
            t = Time()
            t.week = week
            t.day = j


def set_department_table():
    department = ['메카트로닉스공학부', '교양학부', 'HRD학과', ]


def get_users_timetable(request):
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
