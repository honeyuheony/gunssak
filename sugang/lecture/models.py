import django
from django.core.wsgi import get_wsgi_application
from django.db import models


# 수강시간


class Time(models.Model):
    week = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, allow_unicode=True, unique=True)


# 학부
class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, allow_unicode=True, unique=True)


# 분반
class Division(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, allow_unicode=True, unique=True)


# Create your models here.
class Lecture(models.Model):
    name = models.CharField(max_length=100)
    code = models.TextField()
    semester = models.PositiveIntegerField()
    department = models.ManyToManyField(Department, blank=True, null=True)
    credit = models.PositiveIntegerField(default=0)
    time = models.ManyToManyField(Time, blank=True, null=True)
    grade = models.PositiveIntegerField()
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, blank=True, null=True)


class CustomUser(models.Model):
    credit = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    lecture = models.ManyToManyField(Lecture, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.PositiveIntegerField()
