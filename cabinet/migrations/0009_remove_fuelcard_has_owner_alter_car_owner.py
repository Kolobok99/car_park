# Generated by Django 4.0.3 on 2022-04-22 11:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0008_car_image_alter_application_type_of_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fuelcard',
            name='has_owner',
        ),
        migrations.AlterField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), related_name='my_cars', to=settings.AUTH_USER_MODEL),
        ),
    ]