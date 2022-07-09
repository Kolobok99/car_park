# Generated by Django 4.0.3 on 2022-06-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0009_alter_application_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('O', 'Ожидает рассмотрения менеджера'), ('OE', 'Ожидает подтверждение механика'), ('REP', 'Ремонтируется'), ('V', 'Выполнена'), ('P', 'Просрочена'), ('T', 'Отклонено')], default='O', max_length=3, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='historicalapplication',
            name='status',
            field=models.CharField(choices=[('O', 'Ожидает рассмотрения менеджера'), ('OE', 'Ожидает подтверждение механика'), ('REP', 'Ремонтируется'), ('V', 'Выполнена'), ('P', 'Просрочена'), ('T', 'Отклонено')], default='O', max_length=3, verbose_name='Статус'),
        ),
    ]