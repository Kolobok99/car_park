# Generated by Django 4.0.3 on 2022-05-22 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='cabinet.car', verbose_name='Машина'),
        ),
    ]
