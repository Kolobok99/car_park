from django.contrib import admin

from .models import Car, CarBrand, FuelCard,\
                    User, Driver,  Manager, \
                    Document, DriverDoc, AutoDoc, \
                    DocType

# Register your models here.
list_of_moderls = [Car, CarBrand, FuelCard,
                   User, Driver, Manager,
                   DriverDoc, AutoDoc,
                   DocType]

for m in list_of_moderls:
    admin.site.register(m)


