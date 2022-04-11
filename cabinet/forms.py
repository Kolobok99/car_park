from django import forms
from django.core import validators
from django.forms import modelformset_factory

from .models import *


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser
class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MyUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'patronymic',
                  'phone',
                  'role',
                  )
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ('email',)

class CarAddForm(forms.ModelForm):

    # registration_number = forms.CharField(
    #     label='Номер',
    #     validators=[
    #         validators.RegexValidator(
    #             regex='\w{1}\d{3}\w{2}',
    #             message='Введите номер правильно!'
    #         )
    #     ]
    # )
    # brand = forms.ModelChoiceField(label='Марка:', queryset=CarBrand.objects.all()

    # region_code = forms.CharField(label='Код региона:')

    # last_inspection = forms.DateField(label='Последний осмотр:')

    # owner = forms.ModelChoiceField(label='Закрепить за:', queryset=Driver.objects.all())

    class Meta:
        model = Car
        fields = ('registration_number', 'brand', 'region_code', 'last_inspection', 'owner',)
        labels = {
            'registration_number': 'Номер',
            'brand': 'Марка',
            'region_code': 'Код региона',
            'last_inspection': 'Последний осмотр',
            'owner': 'Закрепить за',

        }

class FuelCardAddForm(forms.ModelForm):

    class Meta:
        model = FuelCard
        exclude = ('balance', )

class FuelCardSaltForm(forms.ModelForm):

    class Meta:
        model = FuelCard
        fields = ('has_owner', )

FuelCardSaltSetForm = modelformset_factory(
    FuelCard,
    fields=('has_owner',)
)


class DriverCreateForm(forms.ModelForm):
    '''Форма регистрации пользователя'''
    #
    #
    #
    #
    #
    # password_repeat = forms.CharField(label='Повторите пароль',
    #                                   widget=forms.widgets.PasswordInput(attrs={
    #                                       'placeholder': "повторите пароль"
    #                                   })
    #                                   )
    #
    #
    # class Meta:
    #     model = Driver
    #     fields = (
    #         'user.login',
    #         'user.email',
    #         'user.password',
    #         'password_repeat',
    #
    #         'user.first_name',
    #         'user.last_name',
    #         'user.patronymic',
    #     )
    #
    #     widgets = {
    #         'login': forms.widgets.TextInput(),
    #         'email': forms.widgets.EmailInput(),
    #         'password': forms.widgets.PasswordInput(),
    #         'first_name': forms.widgets.TextInput(),
    #         'last_name': forms.widgets.TextInput(),
    #         'patronymic': forms.widgets.TextInput(),
    #     }
