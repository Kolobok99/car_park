from django.contrib import admin
from django.urls import path

from cabinet.views import CarsView, CarFilterView, FilterCars

urlpatterns = [
    path('filter_cars',FilterCars.as_view(), name='filter_cars' ),
    path('', CarsView.as_view(), name='cars')
    # path('', CarFilterView, name='cars')
]