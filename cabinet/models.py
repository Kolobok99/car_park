from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

class Car(models.Model):
    '''машины водилетей'''

    brand = models.ForeignKey('CarBrand', on_delete=models.SET(1),
                              related_name='cars', verbose_name='Марка')
    registration_number = models.CharField(verbose_name='Регистрационный номер',
                                           unique=True, max_length=5)
    region_code = models.SmallIntegerField(verbose_name='Код региона',
                                           validators=[
                                               MaxValueValidator(200),
                                               MinValueValidator(1)
                                           ])
    onwer = models.ForeignKey('Driver', on_delete=models.PROTECT,
                              related_name='my_cars')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

class CarBrand(models.Model):
    '''марки автомобилей'''

    name = models.CharField(verbose_name='Название бредна', max_length=20)

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

class FuelCard(models.Model):
    '''топливаня карта'''

    limit = models.PositiveIntegerField(verbose_name='лимит')
    number = models.IntegerField(verbose_name='номер', unique=True)

    onwer = models.ForeignKey('Driver', on_delete=models.PROTECT,
                              related_name='my_cards')
    class Meta:
        verbose_name = 'Топливная карта'
        verbose_name_plural = 'Топливные карты'

class User(AbstractUser):
    '''Модель учетная запись пользователей'''

    KINDES = (
        ('a', 'admin'),
        ('m', 'manager'),
        ('d', 'driver'),
    )


    first_name = models.CharField(verbose_name='Имя', max_length=20, null=True, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=20, null=True, blank=True)
    patronymic = models.CharField(verbose_name='Отчество', max_length=20, null=True, blank=True)

    birthdate = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    image = models.ImageField(verbose_name='Аватарка',
                              null=True, blank=True, upload_to=f'avatars/{first_name}+{last_name}')
    email = models.EmailField(verbose_name='Почта', unique=True, null=True, blank=True)

    role = models.CharField(verbose_name='Роль', max_length=1, choices=KINDES, default='d')
    is_staff = models.BooleanField(
        default=False,
    )

class Driver(models.Model):
    '''Водитель'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='d_user')
    phone = models.IntegerField(verbose_name='номер телефона', validators=[
                                               MaxValueValidator(99999999999),
                                               MinValueValidator(10000000000)
                                           ], null=True, blank=True)
    unique_number = models.IntegerField(verbose_name='уникальный номер', db_index=True, validators=[
                                               MaxValueValidator(9999),
                                               MinValueValidator(1)
                                           ], null=True, blank=True)


    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

class Manager(models.Model):
    '''Модель администратора'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='m_user')
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

class Document(models.Model):
    '''абстрактная модель документа'''

    type = None
    created_at = models.DateField(verbose_name='Дата создания',
                                  auto_now_add=True)
    expiration_date = models.DateField(verbose_name='Дата окончания')


    class Meta:
        abstract = True

class DriverDoc(Document):
    '''Документа водителя'''

    type = models.ForeignKey('DocType', on_delete=models.PROTECT,
                             related_name='people_docs')
    owner = models.ForeignKey(Driver, on_delete=models.PROTECT,
                              related_name='doc_owner')
    # def __str__(self):
    #     return f"{self.owner.first_name}"

    class Meta:
        verbose_name = 'Водительский документ'
        verbose_name_plural = 'Водительские документы'

class AutoDoc(Document):
    '''Документа водителя'''

    type = models.ForeignKey('DocType', on_delete=models.PROTECT,
                             related_name='auto_docs')
    owner = models.ForeignKey(Car, on_delete=models.PROTECT,
                              related_name='doc_owner')

    class Meta:
        verbose_name = 'Документ машины'
        verbose_name_plural = 'Документы машины'

class DocType(models.Model):
    '''Тип документа машины'''

    KINDS = (
        ('m', 'Человек'),
        ('с', 'Машина'),
    )

    name = models.CharField(verbose_name='Наименования документа', max_length=20)
    type = models.CharField(max_length=1, choices=KINDS, default='c')

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'

