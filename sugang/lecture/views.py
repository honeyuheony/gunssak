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


def read_exel():
    df = pd.read_exel()
