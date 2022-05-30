from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from cabinet import car_view
from cabinet.views import *
from car_park import settings

urlpatterns = [
    path('cars/', car_view.CarsCreateAndFilterView.as_view(), name='cars'),
    path('cars/<str:slug>', car_view.CarView.as_view(), name='choose-car'),

    path('drivers/', car_view.DriversFilterView.as_view(), name='drivers'),
    path('drivers/<int:pk>', car_view.DriverView.as_view(), name='choose-driver'),

    path('documents/', car_view.DocumentsView.as_view(), name='documents'),

    path('cards/', car_view.CardFilterAndCreateView.as_view(), name='cards'),

    path('applications', car_view.AplicationsView.as_view(), name='applications'),
    path('applications/<int:pk>', car_view.AppView.as_view(), name='app'),

    path('registration/', car_view.RegistrationView.as_view(), name='registration'),
    path('reg-activation/', car_view.EmailConfirmView.as_view(), name='driver-activation'),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html', next_page='login'), name='logout'),

    path('account/', car_view.AccountView.as_view(), name='account'),
    path('history/', car_view.HistoryView.as_view(), name='history'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
