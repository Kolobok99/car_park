# Generated by Django 4.0.3 on 2022-04-25 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0009_remove_fuelcard_has_owner_alter_car_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autodoc',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='userdoc',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
    ]