# Generated by Django 4.0.3 on 2022-03-27 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0007_rename_onwer_car_owner_alter_car_registration_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='onwer',
            new_name='owner',
        ),
    ]
