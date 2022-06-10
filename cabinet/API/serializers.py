import random
import re
import string

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from cabinet.models import Car, MyUser, AutoDoc, UserDoc, FuelCard, Application, WhiteListEmail


class CarSerializer(ModelSerializer):
    """Сериализатор модели Car"""

    class Meta:
        model = Car
        fields = "__all__"

class CarCreateSerializer(ModelSerializer):

    class Meta:
        model = Car
        fields = ('registration_number', 'brand', 'region_code', 'last_inspection', 'owner', 'image')


class DriverSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"

class AutoDocsSerializer(ModelSerializer):
    class Meta:
        model = AutoDoc
        fields = "__all__"

class UserDocsSerializer(ModelSerializer):
    class Meta:
        model = UserDoc
        fields = "__all__"

class FuelCardSerializer(ModelSerializer):
    class Meta:
        model = FuelCard
        fields = "__all__"

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"

def generator_activation_code():
    """Возвращает рандомную строку из 6 символов"""
    letters = string.ascii_lowercase
    length = 6
    rand_string = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", rand_string)
    return rand_string

class RegistrationSerializer(ModelSerializer):
    ROLE_CHOICES = (
        ('d', 'driver'),
        ('e', 'engineer'),
    )

    activation_code = serializers.HiddenField(default=generator_activation_code())
    password_repeat = serializers.CharField(label='Повторите пароль')
    role = serializers.ChoiceField(label="Должность", choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        validated_data = self.validated_data
        # self.instance.set_password(self.validated_data['password'])
        # self.instance.activation_code = self.activation_code

        # cleaned_data = validated_data()
        errors = {}
        email = validated_data.get('email')
        white_emails = [obj.email for obj in WhiteListEmail.objects.all()]

        pass1 = validated_data.get('password')
        pass2 = validated_data.get('password_repeat')

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        patronymic = validated_data.get('patronymic')

        def name_validate(name: str, verbose_name, key):
            if name is not None:
                if not name[0].isupper():
                    errors[key] = ValidationError(f'{verbose_name} должно начинаться с большой буквы!')
                if re.search(r'[a-zA-Z]|\d', name):
                    errors[key] = ValidationError(f'{verbose_name} может состоять только из Кириллицы!')
                if not name.isalpha():
                    errors[key] = ValidationError(f'{verbose_name} может состоять только из Кириллицы!')

        name_validate(first_name, "'имя'", 'first_name')
        name_validate(last_name, "'фамилия'", 'last_name')
        name_validate(patronymic, "'отчество'", 'patronymic')


        if pass1 != pass2:
            errors['password_repeat'] = ValidationError('Пароли не совпадают!')

        # if email not in white_emails:
        #     errors['email'] = ('Ваша почта не указана в списке допустимых. '
        #                        'Обратитесь к администратору')
        if errors:
            raise ValidationError(errors)
        else:
            new_user = MyUser(
                email=email,
                phone=validated_data.get('phone'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                patronymic=validated_data.get('patronymic'),
                role=validated_data.get('role'),
                activation_code=validated_data.get('activation_code')

            )
            new_user.set_password(pass1)
            new_user.save()
            return new_user

    # def save(self, **kwargs):
    #     self.instance.set_password(self.cleaned_data['password'])
    #     self.instance.activation_code = self.activation_code
    #     return super().save(**kwargs)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     errors = {}
    #     email = cleaned_data.get('email')
    #     white_emails = [obj.email for obj in WhiteListEmail.objects.all()]
    #
    #     pass1 = cleaned_data.get('password')
    #     pass2 = cleaned_data.get('password_repeat')
    #
    #     if pass1 != pass2:
    #         errors['password_repeat'] = ValidationError('Пароли не совпадают!')
    #
    #     if email not in white_emails:
    #         errors['email'] = ('Ваша почта не указана в списке допустимых. '
    #                            'Обратитесь к администратору')
    #     if errors:
    #         raise ValidationError(errors)
    #     else:
    #         return cleaned_data

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
            'activation_code',
        )
