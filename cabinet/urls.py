from django.contrib import admin
from django.urls import path

from cabinet.views import CarsView, CarFilterView

urlpatterns = [
    path('', CarsView.as_view(), name='cars')
    # path('', CarFilterView, name='cars')
]