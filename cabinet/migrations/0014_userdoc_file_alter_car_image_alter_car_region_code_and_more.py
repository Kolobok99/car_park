# Generated by Django 4.0.3 on 2022-04-28 05:17

import cabinet.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0013_alter_car_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdoc',
            name='file',
            field=models.FileField(default=1, upload_to=cabinet.models.UserDoc.path_to_upload_file, verbose_name='Копия документа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=cabinet.models.Car.path_to_upload_image, verbose_name='фотография'),
        ),
        migrations.AlterField(
            model_name='car',
            name='region_code',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(200, message='Укажите меньше 200!')], verbose_name='Код региона'),
        ),
        migrations.AlterField(
            model_name='car',
            name='registration_number',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Введите номер правильно!', regex='\\w{1}\\d{3}\\w{2}')], verbose_name='Регистрационный номер'),
        ),
    ]
