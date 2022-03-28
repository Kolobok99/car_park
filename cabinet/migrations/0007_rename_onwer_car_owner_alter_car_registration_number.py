# Generated by Django 4.0.3 on 2022-03-27 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0006_alter_application_options_alter_typeofappl_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='onwer',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='car',
            name='registration_number',
            field=models.CharField(max_length=6, unique=True, verbose_name='Регистрационный номер'),
        ),
    ]