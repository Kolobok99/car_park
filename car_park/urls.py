from django.contrib import admin
from django.urls import path, include

from cabinet import urls as cabinet_urls
from cabinet.API import urls as api_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(cabinet_urls)),
    path("my_api/v1/", include(api_urls))
]
