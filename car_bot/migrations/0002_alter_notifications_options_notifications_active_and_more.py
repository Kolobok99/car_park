# Generated by Django 4.0.3 on 2022-05-30 11:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.AddField(
            model_name='notifications',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активность'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(1), related_name='my_nots', to=settings.AUTH_USER_MODEL, verbose_name='создатель'),
        ),
    ]
