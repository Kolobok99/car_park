from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from cabinet.views import CarsView, DriversView, CarCreateView, DocumentsView, CardCreateView, RegistrationView, CarView

urlpatterns = [
    path('cars/', CarCreateView.as_view(), name='cars'),
    path('cars/<str:slug>', CarView.as_view(), name='choose-car'),
    path('drivers/', DriversView.as_view(), name='drivers'),
    path('documents/', DocumentsView.as_view(), name='documents'),
    path('cards/', CardCreateView.as_view(), name='cards'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html', next_page='login'), name='logout')
]