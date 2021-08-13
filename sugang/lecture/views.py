from django.shortcuts import render
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


def read_exel():
    df = pd.read_exel()


def stanbyPage(request):

    return render(request, "stanbyPage") 

def countDown(request):

    return render(request, "countDown")