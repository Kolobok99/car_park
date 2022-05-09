# Generated by Django 4.0.3 on 2022-05-08 07:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0021_alter_car_registration_number_alter_fuelcard_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autodoc',
            name='owner',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, related_name='my_docs', to='cabinet.car'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^\\d{11}$', 'Номер телефона состоит из 11 цифр')], verbose_name='номер телефона'),
        ),
    ]