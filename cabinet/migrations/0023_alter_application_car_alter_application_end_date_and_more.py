# Generated by Django 4.0.3 on 2022-05-15 10:00

import cabinet.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0022_alter_autodoc_owner_alter_myuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='car',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='cabinet.car', verbose_name='Машина'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='application',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_apps', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='application',
            name='start_date',
            field=models.DateField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='application',
            name='time_to_execute',
            field=models.PositiveIntegerField(default=0, verbose_name='Время на выполнение'),
        ),
        migrations.AlterField(
            model_name='application',
            name='type',
            field=models.ForeignKey(default=1, on_delete=models.SET(1), to='cabinet.typeofappl', verbose_name='Тип заявки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='autodoc',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=cabinet.models.AutoDoc.upload_file, verbose_name='Копия'),
        ),
        migrations.AlterField(
            model_name='autodoc',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_docs', to='cabinet.car', verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='autodoc',
            name='type',
            field=models.ForeignKey(default=1, on_delete=models.SET(1), related_name='auto_docs', to='cabinet.doctype', verbose_name='Тип'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=cabinet.models.Car.path_to_upload_image, verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='car',
            name='last_inspection',
            field=models.DateField(blank=True, null=True, verbose_name='Последний осмотр'),
        ),
        migrations.AlterField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), related_name='my_cars', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='car',
            name='registration_number',
            field=models.CharField(default=1, max_length=6, unique=True, validators=[django.core.validators.RegexValidator(message='Введите номер правильно!', regex='[a-zA-Z]{1}[0-9]{3}[a-zA-Z]{2}')], verbose_name='Регистрационный номер'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='carbrand',
            name='title',
            field=models.CharField(max_length=20, verbose_name='Марка'),
        ),
        migrations.AlterField(
            model_name='doctype',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Наименования'),
        ),
        migrations.AlterField(
            model_name='doctype',
            name='type',
            field=models.CharField(choices=[('m', 'Человек'), ('a', 'Машина')], default='a', max_length=1, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='fuelcard',
            name='balance',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='Остаток'),
        ),
        migrations.AlterField(
            model_name='fuelcard',
            name='limit',
            field=models.PositiveIntegerField(blank=True, verbose_name='Лимит'),
        ),
        migrations.AlterField(
            model_name='fuelcard',
            name='number',
            field=models.CharField(blank=True, max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(16)], verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(default=1, error_messages={'invalid': 'Неправильно совсем!', 'unique': 'Пользователь с таким email уже существует.'}, max_length=254, unique=True, verbose_name='Почта'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(default=1, max_length=20, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(default=1, max_length=20, verbose_name='Фамилия'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='patronymic',
            field=models.CharField(default=1, max_length=20, verbose_name='Отчество'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(default=1, max_length=11, validators=[django.core.validators.RegexValidator('^\\d{11}$', 'Номер телефона состоит из 11 цифр')], verbose_name='Номер телефона'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userdoc',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=cabinet.models.UserDoc.path_to_upload_file, verbose_name='Копия'),
        ),
        migrations.AlterField(
            model_name='userdoc',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_docs', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='userdoc',
            name='type',
            field=models.ForeignKey(default=1, on_delete=models.SET(1), related_name='people_docs', to='cabinet.doctype', verbose_name='Тип'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='HistoricalCar',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('registration_number', models.CharField(db_index=True, max_length=6, validators=[django.core.validators.RegexValidator(message='Введите номер правильно!', regex='[a-zA-Z]{1}[0-9]{3}[a-zA-Z]{2}')], verbose_name='Регистрационный номер')),
                ('region_code', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(200, message='Укажите меньше 200!')], verbose_name='Код региона')),
                ('last_inspection', models.DateField(blank=True, null=True, verbose_name='Последний осмотр')),
                ('image', models.TextField(blank=True, max_length=100, null=True, verbose_name='Фотография')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('brand', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cabinet.carbrand', verbose_name='Марка')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'historical Автомобиль',
                'verbose_name_plural': 'historical Автомобили',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
