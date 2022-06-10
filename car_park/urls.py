from django.contrib import admin
from django.urls import path, include

from cabinet import urls as cabinet_urls
from cabinet.API import urls as api_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(cabinet_urls)),
    path("my_api/v1/", include(api_urls))
]

# #API LESSON 2
# from cabinet.API.lesson2.api_views import CarAPIView
#
# urlpatterns += [
#     path('api/v1/carlist/', CarAPIView.as_view())
# ]

#API LESSON 5
# from cabinet.API.lesson_s.api_view import BrandAPIView
#
# urlpatterns += [
#     path('api/v1/brandlist/', BrandAPIView.as_view()),
#     path('api/v1/brandlist/<int:pk>/', BrandAPIView.as_view())
# ]


# urlpatterns += [
#     path('api/v1/carlist/', CarAPIView.as_view()),
#     path('api/v1/carlist/<int:pk>/', CarAPIView.as_view()),
#
#
#     path('my_api/v1/carlist/', CarListAPIView.as_view()),
#     path('my_api/v1/carcreate/', CarCreateAPIView.as_view()),
#     path('my_api/v1/carupdate/<str:registration_number>/', CarUpdateAPIView.as_view()),
#     path('my_api/v1/carset/owner_none/', MyCarAPIView.as_view({'post': 'owner_none'}))
#
# ]