from django.urls import path, include

from cabinet.API.api import CarAPIViewSet, DriverAPIViewSet, AutoDocsAPIViewSet, DriverDocsAPIViewSet, CardsAPIViewSet, \
    ApplicationsPIViewSet, HistoryAPIViewSet, UserAPIViewSet

urlpatterns = [
    path('cars/list/', CarAPIViewSet.as_view({'get': 'list'})),
    path('cars/filtration', CarAPIViewSet.as_view({'get': 'filtration'})),
    path('cars/create', CarAPIViewSet.as_view({'post': 'create'})),
    path('cars/<str:registration_number>/', CarAPIViewSet.as_view({'get': 'retrieve'})),
    # path('cars/<int:pk>/', CarAPIViewSet.as_view({'get': 'retrieve'})),
    path('cars/update/<str:registration_number>/', CarAPIViewSet.as_view({'patch': 'update'})),
    path('cars/delete/<str:registration_number>/', CarAPIViewSet.as_view({'post': 'destroy'})),
    path("cars/owner_none/", CarAPIViewSet.as_view({"post": 'owner_none'})),
    path("cars/list_to_delete/", CarAPIViewSet.as_view({"post": 'list_to_delete'})),

    path('drivers/list', DriverAPIViewSet.as_view({"get": "list"})),
    path('drivers/filtration', DriverAPIViewSet.as_view({"get": 'filtration'})),
    path('drivers/create', DriverAPIViewSet.as_view({'post': 'create'})),
    path('drivers/<int:pk>/', DriverAPIViewSet.as_view({'get': 'retrieve'})),
    path('drivers/update/<str:registration_number>/', DriverAPIViewSet.as_view({'patch': 'update'})),
    path('drivers/delete/<str:registration_number>/', DriverAPIViewSet.as_view({'post': 'destroy'})),

    # path('all_docs/list', AllDocsAPIViewSet.as_view({'get': 'list'})),

    path('car_docs/list', AutoDocsAPIViewSet.as_view({"get": "list"})),
    path('car_docs/filtation', AutoDocsAPIViewSet.as_view({"get": "filtration"})),
    path('car_docs/create', AutoDocsAPIViewSet.as_view({'post': 'create'})),
    path('car_docs/<str:registration_number>/', AutoDocsAPIViewSet.as_view({'get': 'retrieve'})),
    path('car_docs/update/<str:registration_number>/', AutoDocsAPIViewSet.as_view({'patch': 'update'})),
    path('car_docs/delete/<str:registration_number>/', AutoDocsAPIViewSet.as_view({'post': 'destroy'})),

    path('driver_docs/list/', DriverDocsAPIViewSet.as_view({"get": "list"})),
    path('driver_docs/filtation/', DriverDocsAPIViewSet.as_view({"get": "filtration"})),
    path('driver_docs/create/', DriverDocsAPIViewSet.as_view({'post': 'create'})),
    path('driver_docs/<str:registration_number>/', DriverDocsAPIViewSet.as_view({'get': 'retrieve'})),
    path('driver_docs/update/<str:registration_number>/', DriverDocsAPIViewSet.as_view({'patch': 'update'})),
    path('driver_docs/delete/<str:registration_number>/', DriverDocsAPIViewSet.as_view({'post': 'destroy'})),

    path('cards/list/', CardsAPIViewSet.as_view({"get": "list"})),
    path('cards/filtation/', CardsAPIViewSet.as_view({"get": "filtration"})),

    path('cards/create/', CardsAPIViewSet.as_view({'post': 'create'})),

    path('cards/<str:number>/', CardsAPIViewSet.as_view({'get': 'retrieve'})),

    path('cards/update/<str:number>/', CardsAPIViewSet.as_view({'put': 'partial_update'})),

    path('cards/delete/<str:number>/', CardsAPIViewSet.as_view({'post': 'destroy'})),
    path("cards/owner_none/", CardsAPIViewSet.as_view({"post": 'owner_none'})),
    path("cards/list_to_delete/", CardsAPIViewSet.as_view({"post": 'list_to_delete'})),

    path('apps/list', ApplicationsPIViewSet.as_view({"get": "list"})),
    path('apps/filtation', ApplicationsPIViewSet.as_view({"get": "filtration"})),
    path('apps/create', ApplicationsPIViewSet.as_view({'post': 'create'})),
    path('apps/<str:registration_number>/', ApplicationsPIViewSet.as_view({'get': 'retrieve'})),
    path('apps/update/<str:registration_number>/', ApplicationsPIViewSet.as_view({'patch': 'update'})),
    path('apps/delete/<str:registration_number>/', ApplicationsPIViewSet.as_view({'post': 'destroy'})),

    path('user_logs/list', HistoryAPIViewSet.as_view({"get": "list"})),
    path('user_logs/filtation', HistoryAPIViewSet.as_view({"get": "filtration"})),

    path("user/registration/", UserAPIViewSet.as_view({"post": "create"})),
    path("drf-auth/", include('rest_framework.urls')),
]
