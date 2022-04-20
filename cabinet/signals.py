import os

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from cabinet.models import MyUser


@receiver(post_save, sender=MyUser)
def post_save_myuser(created, **kwargs):
    instance = kwargs['instance']
    if created:
        print(f"{instance.email} создан!")

        #создание папки для пользователя
        os.mkdir(f'{settings.MEDIA_ROOT}/drivers/{instance.email}')

        #создание папки для хранения аватарок
        os.mkdir(f'{settings.MEDIA_ROOT}/drivers/{instance.email}/avatars')

        #создание папки для хранения документов
        os.mkdir(f'{settings.MEDIA_ROOT}/drivers/{instance.email}/docs')