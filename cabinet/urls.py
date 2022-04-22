from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from cabinet.views import *

urlpatterns = [
    path('cars/', CarsCreateAndFilterView.as_view(), name='cars'),
    path('cars/<str:slug>', CarView.as_view(), name='choose-car'),
    # path('cars/<str:slug>/create-app', AppCreateView.as_view(), name='car-create-app'),
    path('drivers/', DriversFilterView.as_view(), name='drivers'),
    path('documents/', DocumentsView.as_view(), name='documents'),
    path('cards/', CardFilterAndCreateView.as_view(), name='cards'),
    path('applications', AplicationsView.as_view(), name='applications'),
    path('applications/<int:pk>', AppView.as_view(), name='app'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html', next_page='login'), name='logout'),
    path('account/', AccountView.as_view(), name='account')
]