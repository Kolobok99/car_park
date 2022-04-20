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
        # os.mkdir(settings.BASE_DIR / f'media/avatars/{instance.email}')
        os.mkdir(f'{settings.MEDIA_ROOT}/avatars/{instance.email}')
