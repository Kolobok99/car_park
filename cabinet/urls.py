from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from cabinet import views
from car_park import settings

urlpatterns = [
    path('cars/', views.CarsCreateAndFilterView.as_view(), name='cars'),
    path('cars/<str:slug>', views.CarView.as_view(), name='choose-car'),

    path('drivers/', views.DriversFilterView.as_view(), name='drivers'),
    path('drivers/<int:pk>', views.DriverView.as_view(), name='choose-driver'),

    path('documents/', views.DocumentsView.as_view(), name='documents'),

    path('cards/', views.CardFilterAndCreateView.as_view(), name='cards'),

    path('applications', views.AplicationsView.as_view(), name='applications'),
    path('applications/<int:pk>', views.AppView.as_view(), name='app'),

    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('reg-activation/', views.EmailConfirmView.as_view(), name='driver-activation'),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html', next_page='login'), name='logout'),

    path('account/', views.AccountView.as_view(), name='account'),
    path('history/', views.HistoryView.as_view(), name='history'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
