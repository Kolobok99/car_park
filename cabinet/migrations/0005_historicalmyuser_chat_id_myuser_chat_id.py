# Generated by Django 4.0.3 on 2022-06-01 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0004_historicalmyuser_activation_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmyuser',
            name='chat_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='chat_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
