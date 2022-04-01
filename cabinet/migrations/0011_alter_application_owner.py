# Generated by Django 4.0.3 on 2022-03-29 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0010_application_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='my_apps', to='cabinet.driver'),
        ),
    ]