from django.contrib import admin
from django.urls import path

from cabinet.views import CarsView, DriversView, CarCreateView

urlpatterns = [
    path('car/create', CarCreateView.as_view(), name='car-create'),
    path('cars/', CarCreateView.as_view(), name='cars'),
    path('drivers/', DriversView.as_view(), name='drivers'),
]