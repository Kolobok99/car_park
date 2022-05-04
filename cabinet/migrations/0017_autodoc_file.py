# Generated by Django 4.0.3 on 2022-05-03 09:08

import cabinet.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0016_application_manager_descr_alter_application_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='autodoc',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=cabinet.models.AutoDoc.upload_file, verbose_name='Копия документа'),
        ),
    ]
