import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.core import validators

from datetime import timedelta

from django.db.models import Q


class Car(models.Model):
    '''машины водилетей'''

    brand = models.ForeignKey('CarBrand', on_delete=models.SET_NULL,
                              related_name='cars', verbose_name='Марка', null=True, blank=True)
    registration_number = models.CharField(verbose_name='Регистрационный номер',
                                           unique=True, max_length=6, validators=[
            validators.RegexValidator(
                regex='\w{1}\d{3}\w{2}',
                message='Введите номер правильно!'
            )], )
    region_code = models.PositiveSmallIntegerField(verbose_name='Код региона',
                                                   validators=[
                                                       validators.MaxValueValidator(200, message='Укажите меньше 200!')]
                                                   )
    owner = models.ForeignKey('MyUser', on_delete=models.SET_NULL,
                              related_name='my_cars', null=True, blank=True)

    last_inspection = models.DateField("последний осмотр", null=True, blank=True)

    def save(self, *args, **kwargs):
        # self.slug = self.registration_number
        self.registration_number = self.registration_number.upper()
        super(Car, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/cars/{self.registration_number}"

    def __str__(self):
        return f"{self.registration_number}"

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class CarBrand(models.Model):
    '''марки автомобилей'''

    name = models.CharField(verbose_name='Название бредна', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class FuelCard(models.Model):
    '''топливаня карта'''

    limit = models.PositiveIntegerField(verbose_name='лимит')
    number = models.CharField(verbose_name='номер', unique=True, max_length=16,
                              validators=[validators.MinLengthValidator(16)])

    owner = models.ForeignKey('MyUser', on_delete=models.SET_NULL,
                              related_name='my_cards', blank=True, null=True)

    balance = models.PositiveIntegerField(verbose_name='остаток', default=None, null=True, blank=True)

    has_owner = models.BooleanField('Есть владелец?', default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.balance is None:
            self.balance = self.limit
        super().save(*args, **kwargs)
        if self.owner is not None:
            self.has_owner = True

    class Meta:
        verbose_name = 'Топливная карта'
        verbose_name_plural = 'Топливные карты'


class MyUserManager(BaseUserManager):
    """Менеджер для модели MyUser"""

    def create_user(self, email, password, **extra_fields):
        """Создание и сохранение записи в таблице MyUser"""
        if not email:
            raise ValueError("Укажите Email!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return MyUser

    def create_superuser(self, email, password, **extra_fields):
        """Создание и сохранение root'а """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Root должен иметь is_staph=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Root должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    '''Модель учетная запись пользователей'''

    KINDES = (
        ('a', 'admin'),
        ('m', 'manager'),
        ('d', 'driver'),
    )
    email = models.EmailField(verbose_name='Почта', unique=True, null=True, blank=True)
    password = models.CharField("Пароль", max_length=128, )

    first_name = models.CharField(verbose_name='Имя', max_length=20, null=True, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=20, null=True, blank=True)
    patronymic = models.CharField(verbose_name='Отчество', max_length=20, null=True, blank=True)
    phone = models.CharField(verbose_name='номер телефона', null=True, blank=True, max_length=12)

    image = models.ImageField(verbose_name='Аватарка',
                              null=True, blank=True, upload_to=f'avatars/')

    role = models.CharField(verbose_name='Роль', max_length=1, choices=KINDES, default='d')

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def is_manager(self):
        if self.role == 'm':
            return True
        else:
            return False

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Document(models.Model):
    '''абстрактная модель документа'''

    type = None
    created_at = models.DateField(verbose_name='Дата создания',
                                  auto_now_add=True)
    date_start = models.DateField(verbose_name='Дата выдачи')
    date_end = models.DateField(verbose_name='Дата окончания')

    class Meta:
        abstract = True



class UserDoc(Document):
    '''Документа водителя'''

    type = models.ForeignKey('DocType', on_delete=models.SET_NULL,
                             related_name='people_docs', null=True, blank=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                              related_name='my_docs')

    def __str__(self):
        return f"{self.type} - {self.owner}"

    class Meta:
        verbose_name = 'Водительский документ'
        verbose_name_plural = 'Водительские документы'


class AutoDoc(Document):
    '''Документа водителя'''

    type = models.ForeignKey('DocType', on_delete=models.SET_NULL,
                             related_name='auto_docs', null=True, blank=True)
    owner = models.ForeignKey(Car, on_delete=models.CASCADE,
                              related_name='my_docs')
    def __str__(self):
        return f"{self.type} - {self.owner}"

    class Meta:
        verbose_name = 'Документ машины'
        verbose_name_plural = 'Документы машины'


class DocType(models.Model):
    '''Тип документа машины'''

    KINDS = (
        ('m', 'Человек'),
        ('a', 'Машина'),
    )

    name = models.CharField(verbose_name='Наименования документа', max_length=255)
    type = models.CharField(max_length=1, choices=KINDS, default='a')

    def __str__(self):
        return f'{self.name} ({self.type})'

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'


class Application(models.Model):
    """Заявки на ремонт"""

    STATUS_CHOISES = (
        ('O', 'Ожидает рассмотрения'),
        ('R', 'Рассмотрена'),
        ('V', 'Выполнена'),
        ('P', 'Просрочена'),
    )

    URGENCY_CHOISES = (
        ('N', 'Не срочно'),
        ('U', 'Срочно'),
        ('S', 'Очень срочно'),
    )

    type_of = models.ForeignKey("TypeOfAppl", on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='my_apps')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    start_date = models.DateField(verbose_name='время создания', auto_now_add=True)
    time_to_execute = models.PositiveIntegerField(verbose_name='время на выполнение',
                                                  default=7)
    end_date = models.DateField(verbose_name='дата окончания', null=True, blank=True)

    is_active = models.BooleanField(verbose_name="Активность заявки", default=True)
    status = models.CharField(verbose_name='Статус', max_length=1, choices=STATUS_CHOISES, default='o')
    urgency = models.CharField(verbose_name='Cрочность', max_length=1, choices=URGENCY_CHOISES, default='N')

    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.owner.last_name} + " \
               f"{self.start_date} + {self.type_of} + {self.car.registration_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.time_to_execute == 0:
            if self.urgency == 'N':
                self.end_date = self.start_date + timedelta(days=10)
            elif self.urgency == 'U':
                self.end_date = self.start_date + timedelta(days=7)
            elif self.urgency == 'V':
                self.end_date = self.start_date + timedelta(days=3)
        else:
            self.end_date = self.start_date + timedelta(days=self.time_to_execute)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class TypeOfAppl(models.Model):
    """Типы заявок"""

    title = models.CharField(verbose_name='Наименование', max_length=50)
    car_is = models.BooleanField(verbose_name='Машина или Сотрудник', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'
