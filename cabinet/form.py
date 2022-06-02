import re
from django import forms

from .models import *
# from django.core.exceptions import ValidationError as ValEr, FieldError

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser


# -----------------------  ADMIN -----------------------

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

# -----------------------  CAR -----------------------

class CarForm(forms.ModelForm):
    """Базовая форма машины"""

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

class CarAddForm(CarForm):
    """
        Форма: добавление новой машины
    """
    ...

class CarUpdateForm(CarForm):
    """
        Форма: обновление данных машины
    """
    action = forms.CharField(widget=forms.HiddenInput(), initial="car_update")

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        list_of_fields = ['registration_number', 'brand', 'region_code',
                          'last_inspection']
        print("cleaned-last: ", self.cleaned_data['last_inspection'])
        print("self-last: ", self.car.last_inspection)
        for field in list_of_fields:
            if self.cleaned_data[field] is None:
                setattr(self.instance, field, getattr(self.car, field))

        return super().save(**kwargs)


# -----------------------  DRIVER -----------------------

class UserCreateForm(forms.ModelForm):
    """
        Форма: регистрация пользователя
    """

    ROLE_CHOICES = (
        ('d', 'driver'),
        ('e', 'engineer'),
    )

    def __init__(self, *args, **kwargs):
        self.activation_code = kwargs.pop('activation_code', None)
        super().__init__(*args, **kwargs)

    password_repeat = forms.CharField(label='Повторите пароль',
                                      widget=forms.widgets.PasswordInput()
                                      )
    role = forms.ChoiceField(label="Должность", choices=ROLE_CHOICES)
    def save(self, **kwargs):
        self.instance.set_password(self.cleaned_data['password'])
        self.instance.activation_code = self.activation_code
        return super().save(**kwargs)

    def clean(self):
        cleaned_data = super().clean()
        errors = {}
        email = cleaned_data.get('email')
        white_emails = [obj.email for obj in WhiteListEmail.objects.all()]

        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('password_repeat')

        if pass1 != pass2:
            errors['password_repeat'] = ValidationError('Пароли не совпадают!')

        if email not in white_emails:
            errors['email'] = ('Ваша почта не указана в списке допустимых. '
                                              'Обратитесь к администратору')
        if errors:
            raise ValidationError(errors)
        else:
            return cleaned_data

    class Meta:
        model = MyUser
        fields = (
            'email',
            'password',
            'password_repeat',
            'phone',
            'first_name',
            'last_name',
            'patronymic',
            'role',
        )

        widgets = {
            'email': forms.widgets.EmailInput(),
            'password': forms.widgets.PasswordInput(),
            'first_name': forms.widgets.TextInput(),
            'last_name': forms.widgets.TextInput(),
            'patronymic': forms.widgets.TextInput(),
        }


class UserUpdateForm(forms.ModelForm):
    """
        Форма: обновление данных пользователя
    """

    action = forms.CharField(widget=forms.HiddenInput(), initial="user_update")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        """Заполняет пустые поля формы"""
        list_of_fields = ['first_name', 'last_name', 'patronymic',
                          'phone', 'email']
        for field in list_of_fields:
            if self.cleaned_data[field] is None:
                setattr(self.instance, field, getattr(self.user, field))
        return super().save(**kwargs)

    class Meta:
        model = MyUser
        exclude = ('role', 'is_active', 'is_staff', 'is_superuser', 'password')


class DriverActivationForm(forms.Form):
    """
        Форма: подтверждение регистрации
    """

    activation_code = forms.CharField(label="Код подтверждение")

# -----------------------  CARD -----------------------

class FuelCardAddForm(forms.ModelForm):
    """
        Форма: добавление данных
    """

    owner = forms.ModelChoiceField(queryset=MyUser.objects.filter(my_card__isnull=True), required=False)

    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        if not cleaned_data['number'].isdigit():
            errors['number'] = ValidationError('номер карты может состоять только из цифр!')
        if errors:
            raise ValidationError(errors)
        return cleaned_data


    class Meta:
        model = FuelCard
        exclude = ('balance', )

        # error_messages = widgets()

class FuelCardChangeBalance(forms.ModelForm):

    """
        Форма: изменение баланса карты
    """

    action = forms.CharField(widget=forms.HiddenInput(), initial="change_balance")

    class Meta:
        model = FuelCard
        fields = ('balance', )

# -----------------------  APP -----------------------


class AppForm(forms.ModelForm):

    """
        Базовая форма заявки
    """

    class Meta:
        model = Application
        fields = ('type',
                  'urgency',
                  'description',
                  )
        widgets = {
            'urgency': forms.widgets.RadioSelect(),
        }

class AppCreateForm(AppForm):
    """
        Форма: создание заявки
    """

    action = forms.CharField(widget=forms.HiddenInput(), initial="app_create")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.instance.owner = self.user
        self.instance.car = self.car
        if self.user.is_manager(): self.instance.status = 'R'
        return super(AppForm, self).save()

class AppUpdateForm(AppForm):
    """
        Форма: обновление заявки
    """

    action = forms.CharField(widget=forms.HiddenInput(), initial="app_update")

class ManagerCommitAppForm(forms.ModelForm):
    """
        Форма: подтверждение заявки (менеджером)
    """

    action = forms.CharField(widget=forms.HiddenInput(), initial="app_confirm")

    engineer = forms.ModelChoiceField(queryset=MyUser.objects.filter(role='e'), required=True, label='Выберите инженера')

    def save(self, **kwargs):
        self.instance.status = 'R'
        return super(ManagerCommitAppForm, self).save(**kwargs)



    class Meta:
        model = Application
        fields = ('manager_descr', 'engineer')

# -----------------------  DOC -----------------------

class AutoDocForm(forms.ModelForm):

    """
        Форма: добавление документа (авто)
    """

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)

    action = forms.CharField(widget=forms.widgets.HiddenInput(), initial="doc_create")


    def save(self, **kwargs):
        self.instance.owner = self.car
        return super(AutoDocForm, self).save(**kwargs)

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
    """
        Форма: добавление документа (водитель)
    """

    action = forms.CharField(widget=forms.widgets.HiddenInput(), initial='doc_create')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.instance.owner = self.user
        return super(DriverDocForm, self).save(**kwargs)


    class Meta:
        model = UserDoc
        exclude = ('owner',)
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={
                "type": 'date',

            }),
            'end_date': forms.widgets.DateInput(attrs={
                "type": 'date',

            }),
            'type': forms.widgets.RadioSelect(

            )
        }

