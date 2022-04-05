from django.contrib import admin
from django.urls import path

from cabinet.views import CarsView, DriversView, CarCreateView

urlpatterns = [
    path('cars/', CarsView.as_view(), name='cars'),
    path('drivers/', DriversView.as_view(), name='drivers'),
    path('cars/create', CarCreateView.as_view(), name='create-car')
]