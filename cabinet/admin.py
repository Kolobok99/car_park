from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cabinet.forms import MyUserCreationForm, MyUserChangeForm
from cabinet import models
from car_bot import models as bot_models
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
list_of_models = [models.Car, models.CarBrand, models.FuelCard,
                  models.UserDoc, models.AutoDoc, models.DocType,
                  models.Application, models.TypeOfAppl, models.WhiteListEmail, bot_models.Notifications]
for m in list_of_models:
    admin.site.register(m, SimpleHistoryAdmin)

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = models.MyUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'patronymic', 'phone', 'role', 'activation_code', 'chat_id')}),
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


admin.site.register(models.MyUser, MyUserAdmin)