from django.contrib import admin
from django.urls import path

from cabinet.views import CarsView, DriversView

urlpatterns = [
    path('cars/', CarsView.as_view(), name='cars'),
    path('drivers/', DriversView.as_view(), name='drivers'),
]