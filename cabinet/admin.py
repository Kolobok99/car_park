from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from car_bot.models import Notifications
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from .early_forms import *
# Register your models here.
list_of_moderls = [Car, CarBrand, FuelCard,
                   UserDoc, AutoDoc, DocType,
                   Application, TypeOfAppl, WhiteListEmail, Notifications]
for m in list_of_moderls:
    admin.site.register(m, SimpleHistoryAdmin)

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'patronymic', 'phone', 'role', 'activation_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'patronymic', 'phone', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(MyUser, MyUserAdmin)