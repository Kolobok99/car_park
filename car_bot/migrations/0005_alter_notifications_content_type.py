# Generated by Django 4.0.3 on 2022-06-28 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('car_bot', '0004_notifications_owner_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='content_type',
            field=models.ForeignKey(on_delete=models.SET(1), to='contenttypes.contenttype'),
        ),
    ]