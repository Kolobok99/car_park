import datetime
import re
from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core import validators
from rest_framework.exceptions import ValidationError as restValid

from simple_history.models import HistoricalRecords


class Car(models.Model):
    """
        Модель: машины
    """

    def path_to_upload_image(self, *args):
        """Возвращает путь загрузки фотографии"""
        path = f"cars/{self.registration_number}/avatars/car_avatar"
        return path

    brand = models.ForeignKey('CarBrand', verbose_name='Марка', on_delete=models.SET(1),
                              related_name='cars')
    registration_number = models.CharField('Регистрационный номер',
                                           unique=True, max_length=6,
                                           validators=[
                                               validators.RegexValidator(
                                                   regex='[a-zA-Z]{1}[0-9]{3}[a-zA-Z]{2}',
                                                   message='Введите номер правильно!'
                                               )])

    region_code = models.PositiveSmallIntegerField('Код региона',
                                                   validators=[
                                                       validators.MaxValueValidator(
                                                           200,
                                                           message='Укажите меньше 200!'
                                                       )])
    owner = models.ForeignKey('MyUser', verbose_name='Владелец', on_delete=models.SET(None),
                              related_name='my_cars', null=True, blank=True)

    last_inspection = models.DateField("Последний осмотр", null=True, blank=True)

    image = models.ImageField('Фотография', null=True, blank=True, upload_to=path_to_upload_image)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        """Сжимает изображение"""
        super(Car, self).save(**kwargs)
        try:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path, 'png')
        except:
            pass

    def get_absolute_url(self):
        return f"/cars/{self.registration_number}"

    def __str__(self):
        return f"{self.registration_number}"

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class CarBrand(models.Model):
    """
        Модель: марки автомобилей
    """

    title = models.CharField(verbose_name='Марка', max_length=20, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class FuelCard(models.Model):
    """топливные карты"""


    limit = models.PositiveIntegerField('Лимит', blank=True)
    number = models.CharField('Номер', unique=True, max_length=16, blank=True,
                              validators=[
                                  validators.RegexValidator(
                                      "^\d{16}$",
                                      "Номер топливной карты состоит из 16 цифр"
                                  )],)

    owner = models.OneToOneField('MyUser', verbose_name='Владелец', on_delete=models.SET_NULL,
                                 related_name='my_card', blank=True, null=True)

    balance = models.PositiveIntegerField('Остаток', default=None, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        # 1234-5678-1234-5678
        return f"{self.number[0:4]}-{self.number[4:8]}-{self.number[8:12]}-{self.number[12:16]}"

    class Meta:
        verbose_name = 'Топливная карта'
        verbose_name_plural = 'Топливные карты'


class MyUserManager(BaseUserManager):
    """
        Менеджер: модели MyUser
    """

    def create_user(self, email, password, **extra_fields):
        """ Создание user'а """
        if not email:
            raise ValueError("Укажите Email!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return MyUser

    def create_superuser(self, email, password, **extra_fields):
        """Создание root'а """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Root должен иметь is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Root должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
        Модель: Пользователя
    """
    # Типы user'ов
    KINDES = (
        ('a', 'admin'),
        ('m', 'manager'),
        ('d', 'driver'),
        ('e', 'engineer'),
    )

    def path_to_upload_image(self, *args):
        """Возвращает путь загрузки фотографии"""
        path = f"drivers/{self.email}/avatars/user_avatar{datetime.datetime.today()}.webp"
        return path

    email = models.EmailField('Почта', unique=True,
                              error_messages={
                                  'unique': 'Пользователь с таким email уже существует.',
                                  'invalid': 'Неправильно совсем!'
                              })
    password = models.CharField("Пароль", max_length=128)

    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20, )
    patronymic = models.CharField('Отчество', max_length=20)
    phone = models.CharField('Номер телефона', max_length=11, unique=True, validators=[
        validators.RegexValidator("^\d{11}$", "Номер телефона состоит из 11 цифр"),

    ])

    image = models.ImageField('Аватарка', null=True, blank=True, upload_to=path_to_upload_image)

    role = models.CharField('Роль', max_length=1, choices=KINDES, default='d')

    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    history = HistoricalRecords()

    chat_id = models.PositiveIntegerField("ID телеграмм чата", null=True, blank=True, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def save(self):
        """Сжимает фотографии"""
        super().save()
        try:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path, 'png')
        except:
            pass
        super(MyUser, self).save()

    # заглушка для избежания ошибок переопределения AbstractBaseUser
    last_login = None
    def update_last_login(sender, user, **kwargs):
        pass

    def is_manager(self):
        if self.role == 'm':
            return True
        return False

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_absolute_url(self):
        return f"/drivers/{self.pk}"

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        errors = {}

        first_name = self.first_name
        last_name = self.last_name
        patronymic = self.patronymic

        def name_validate(name: str, verbose_name, key):
            """Валидирует имя, фамилию, отчество"""
            if name is not None:
                if not name[0].isupper():
                    errors[key] = ValidationError(f'{verbose_name} должно начинаться с большой буквы!')
                if re.search(r'[a-zA-Z]|\d', name):
                    errors[key] = ValidationError(f'{verbose_name} может состоять только из Кириллицы!')
                if not name.isalpha():
                    errors[key] = ValidationError(f'{verbose_name} может состоять только из Кириллицы!')

        name_validate(first_name, "имя", 'first_name')
        name_validate(last_name, "фамилия", 'last_name')
        name_validate(patronymic, "отчество", 'patronymic')

        if errors:
            # Вызывает ValidationError (from DRF)
            try:
                raise restValid(errors)
            except:
                # Если метод вызван из обычной формы,
                # вызывает стандартную ValidationError (from django.core.exceptions)
                raise ValidationError(errors)
        return cleaned_data

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Document(models.Model):
    """
        Модель: Абстрактная модель документа
    """

    type = None
    created_at = models.DateField('Дата добавления', auto_now_add=True)
    start_date = models.DateField('Дата выдачи')
    end_date = models.DateField('Дата окончания')

    history = HistoricalRecords(inherit=True)

    def clean(self):
        errors = {}
        cleaned_data = super().clean()
        if self.start_date > self.end_date:
            errors['start_date'] = ValidationError("Дата окончания меньше даты выпуска")

        if errors:
            # Вызывает ValidationError (from DRF)
            try:
                raise restValid(errors)
            except:
                # Если метод вызван из обычной формы,
                # вызывает стандартную ValidationError (from django.core.exceptions)
                raise ValidationError(errors)
        return cleaned_data

    class Meta:
        abstract = True


class UserDoc(Document):
    """
        Модель: Документы водителя
    """

    def path_to_upload_file(self, *args):
        """Возвращает путь загрузки документа"""
        path = f"drivers/{self.owner.email}/docs/user_doc_{self.type}_{self.end_date}"
        return path

    type = models.ForeignKey('DocType', verbose_name="Тип", on_delete=models.SET(1),
                             related_name='people_docs')
    owner = models.ForeignKey(MyUser, verbose_name="Владелец", on_delete=models.CASCADE,
                              related_name='my_docs')
    file = models.FileField('Копия', upload_to=path_to_upload_file, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.owner}"

    class Meta:
        verbose_name = 'Водительский документ'
        verbose_name_plural = 'Водительские документы'


class AutoDoc(Document):
    """
        Модель: Документа водителя
    """

    def upload_file(self, *args):
        """Возвращает путь загрузки документа"""
        path = f"cars/{self.owner.registration_number}/docs/car_doc_{self.type}_{self.end_date}"
        return path

    type = models.ForeignKey('DocType', verbose_name="Тип", on_delete=models.SET(1),
                             related_name='auto_docs')
    owner = models.ForeignKey(Car, verbose_name="Владелец", on_delete=models.CASCADE,
                              related_name='my_docs')
    file = models.FileField('Копия', upload_to=upload_file, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.owner}"

    class Meta:
        verbose_name = 'Документ машины'
        verbose_name_plural = 'Документы машины'


class DocType(models.Model):
    """
        Модель: Тип документа машины
    """

    KINDS = (
        ('m', 'Человек'),
        ('a', 'Машина'),
    )

    title = models.CharField('Наименования', max_length=255)
    type = models.CharField("Тип", max_length=1, choices=KINDS, default='a')

    def __str__(self):
        return f'{self.title} ({self.type})'

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'


class Application(models.Model):
    """
        Модель: Заявки на ремонт
    """

    STATUS_CHOISES = (
        ('O', 'Ожидает рассмотрения менеджера'),
        ('OE', "Ожидает подтверждение механика"),
        ("REP", "Ремонтируется"),
        ('V', 'Выполнена'),
        ('P', 'Просрочена'),
        ('T', 'Отклонено')
    )

    URGENCY_CHOISES = (
        ('N', 'Не срочно'),
        ('U', 'Срочно'),
        ('S', 'Очень срочно'),
    )

    type = models.ForeignKey("TypeOfAppl", verbose_name='Тип заявки', on_delete=models.SET(1))
    owner = models.ForeignKey(MyUser, verbose_name='Владелец', on_delete=models.SET_NULL, related_name='my_apps', null=True)
    engineer = models.ForeignKey(MyUser, verbose_name='Механик', on_delete=models.SET_NULL,related_name='my_repair_apps', null=True)
    car = models.ForeignKey(Car, verbose_name="Машина", on_delete=models.CASCADE, related_name='applications')
    start_date = models.DateField('Время создания', auto_now_add=True)
    time_to_execute = models.PositiveIntegerField('Время на выполнение',
                                                  default=0)
    end_date = models.DateField('Дата окончания', null=True, blank=True)

    is_active = models.BooleanField("Активность заявки", default=True)
    status = models.CharField('Статус', max_length=3, choices=STATUS_CHOISES, default='O')
    urgency = models.CharField('Cрочность', max_length=1, choices=URGENCY_CHOISES, default='N')

    description = models.TextField("Описание")
    manager_descr = models.TextField("Комментарий менеджера", null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        if self.owner:
            return f"{self.pk}-{self.owner.last_name} + " \
                   f"{self.start_date} + {self.type} + {self.car.registration_number}"
        else:
            return f"{self.pk}"
    def get_absolute_url(self):
        return f"/applications/{self.pk}"


    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class TypeOfAppl(models.Model):
    """
        Модель: Типы заявок
    """

    title = models.CharField('Наименование', max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'


class WhiteListEmail(models.Model):
    """
        Модель: Чек лист разрешенных для регистрации email'ов
    """

    email = models.EmailField('Email')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'White List of Emil'
        verbose_name_plural = 'White List of Emil'

