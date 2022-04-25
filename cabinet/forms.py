import re

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
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

    last_inspection = forms.DateField(label='Последний осмотр:', widget=forms.DateInput(attrs={'class':'datepicker form-control', 'placeholder':'Select a date'}), required=False)

    # owner = forms.ModelChoiceField(label='Закрепить за:', queryset=Driver.objects.all())


    class Meta:
        model = Car
        fields = ('registration_number', 'brand', 'region_code', 'last_inspection', 'owner', 'image')
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

# class FuelCardSaltForm(forms.ModelForm):
#
#     class Meta:
#         model = FuelCard
#         fields = ('has_owner', )

class UserCreateForm(forms.ModelForm):
    '''Форма регистрации пользователя'''
    password_repeat = forms.CharField(label='Повторите пароль',
                                      widget=forms.widgets.PasswordInput()
                                      )

    def clean(self):
        cleaned_data = super().clean()
        errors = {}
        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('password_repeat')

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        patronymic = cleaned_data.get('patronymic')

        def name_validate(name:str, verbose_name, key):
            if not name[0].isupper():
                errors[key] = ValidationError(f'{verbose_name} должно начинаться с большой буквы!')
            if re.search(r'[a-zA-Z]|\d', name):
                errors[key] = ValidationError(f'{verbose_name} может состоять только из Кириллицы!')

        if pass1 != pass2:
            errors['password'] = ValidationError('Пароли не совпадают!')

        name_validate(first_name, "'имя'", 'first_name')
        name_validate(last_name, "'фамилия'", 'last_name')
        name_validate(patronymic, "'отчество'", 'patronymic')

        if errors:
            raise ValidationError(errors)
        return cleaned_data

    class Meta:
        model = MyUser
        fields = (
            'email',
            'password',
            'password_repeat',
            'first_name',
            'last_name',
            'patronymic',

        )

        widgets = {
            'login': forms.widgets.TextInput(),
            'email': forms.widgets.EmailInput(),
            'password': forms.widgets.PasswordInput(),
            'first_name': forms.widgets.TextInput(),
            'last_name': forms.widgets.TextInput(),
            'patronymic': forms.widgets.TextInput(),
        }

class UserUpdateForm(forms.ModelForm):
    #
    # def __init__(self, *args, **kwargs):
    #     super(UserUpdateForm, self).__init__(*args, **kwargs)
    #     self.fields['first_name'].widget = forms.widgets.TextInput(
    #         attrs={
    #             "placeholder": self.fields['first_name'].value
    #         }
    #     )

    class Meta:
        model = MyUser
        exclude = ('role','is_active', 'is_staff', 'is_superuser', 'image', 'password')
        # widgets = {
        #     'first_name': forms.widgets.TextInput(
        #         attrs={
        #             'placeholder':
        #         }
        #     )
        # }



class AppForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Не выбран"

    # action = forms.CharField(widget=forms.HiddenInput(), initial="app_create")

    class Meta:
        model = Application
        fields = ('type',
                  'urgency',
                  'description',
                  # 'car',
                  # 'owner',
                  # 'status'
                  )
        widgets = {
            # 'car': forms.widgets.HiddenInput(),
            # 'owner': forms.widgets.HiddenInput(),
            # 'status': forms.widgets.HiddenInput(),
            'urgency': forms.widgets.RadioSelect(),
        }

class AppCreateForm(AppForm):
    action = forms.CharField(widget=forms.HiddenInput(), initial="app_create")

class AppUpdateForm(AppForm):
    action = forms.CharField(widget=forms.HiddenInput(), initial="app_update")


class AutoDocForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Не выбран"

    action = forms.CharField(widget=forms.widgets.HiddenInput(), initial="doc_create")
    class Meta:
        model = AutoDoc
        # fields = '__all__'
        exclude = ('owner',)
        widgets = {
            # 'owner': forms.widgets.HiddenInput(),
            'start_date': forms.widgets.DateInput(attrs={
                "type": 'date',

            }),
            'end_date': forms.widgets.DateInput(attrs={
                "type": 'date',

            }),
            'type': forms.widgets.RadioSelect(

            )
        }


class DriverDocForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Не выбран"

    action = forms.CharField(widget=forms.widgets.HiddenInput())
    class Meta:
        model = UserDoc
        # fields = '__all__'
        exclude = ('owner',)
        widgets = {
            # 'owner': forms.widgets.HiddenInput(),
            'start_date': forms.widgets.DateInput(attrs={
                "type": 'date',

            }),
            'end_date': forms.widgets.DateInput(attrs={
                "type": 'date',

            }),
            'type': forms.widgets.RadioSelect(

            )
        }

