# Generated by Django 4.0.3 on 2022-04-26 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0012_alter_car_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cars', verbose_name='фотография'),
        ),
    ]
