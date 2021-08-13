from django.contrib import admin
from .models import Time, Department, Lecture, CustomUser


# Register your models here.
admin.site.register(Time)
admin.site.register(Department)
admin.site.register(Lecture)
admin.site.register(CustomUser)
