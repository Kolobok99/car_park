from django.contrib import admin
from django.urls import path

from cabinet.views import CarsView, DriversView, CarCreateView, DocumentsView, CardCreateView

urlpatterns = [
    # path('car/create', CarCreateView.as_view(), name='car-create'),
    path('cars/', CarCreateView.as_view(), name='cars'),
    path('drivers/', DriversView.as_view(), name='drivers'),
    path('documents/', DocumentsView.as_view(), name='documents'),
    path('cards/', CardCreateView.as_view(), name='cards'),
]