# Generated by Django 4.0.3 on 2022-05-01 05:35

import cabinet.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0014_userdoc_file_alter_car_image_alter_car_region_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhiteListEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'White List of Emil',
                'verbose_name_plural': 'White List of Emil',
            },
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='last_login',
        ),
        migrations.AlterField(
            model_name='fuelcard',
            name='limit',
            field=models.PositiveIntegerField(blank=True, verbose_name='лимит'),
        ),
        migrations.AlterField(
            model_name='fuelcard',
            name='number',
            field=models.CharField(blank=True, max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(16)], verbose_name='номер'),
        ),
        migrations.AlterField(
            model_name='userdoc',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=cabinet.models.UserDoc.path_to_upload_file, verbose_name='Копия документа'),
        ),
    ]
