from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [

    path('admin/', admin.site.urls),
    path('stanbyPage/',stanbyPage,name="stanbyPage"),
    path('countDown/',countDown,name="countDown"),
]