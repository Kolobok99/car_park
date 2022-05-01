from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *
# Register your models here.
list_of_moderls = [Car, CarBrand, FuelCard,
                   UserDoc, AutoDoc, DocType,
                   Application, TypeOfAppl, WhiteListEmail]
for m in list_of_moderls:
    admin.site.register(m)

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'patronymic', 'phone', 'role')}),
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