# Generated by Django 4.0.3 on 2022-03-20 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0002_alter_driver_managers_alter_manager_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autodoc',
            name='file',
        ),
        migrations.RemoveField(
            model_name='driverdoc',
            name='file',
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/<django.db.models.fields.CharField>+<django.db.models.fields.CharField>', verbose_name='Аватарка'),
        ),
    ]
