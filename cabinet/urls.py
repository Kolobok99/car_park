from django.contrib import admin
from django.urls import path

from cabinet.views import CarsView

urlpatterns = [
    path('', CarsView.as_view(), name='cars')
]