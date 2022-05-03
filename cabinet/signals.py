import os

from django.core.files import File
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings

from cabinet.models import MyUser, Car


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

@receiver(pre_save, sender=MyUser)
def pre_save_myuser(instance, **kwargs):
    if not (instance._state.adding):
        old_user = MyUser.objects.get(pk=instance.pk)
        old_email = old_user.email

        if instance.email != old_email:
            os.renames(
                f'{settings.MEDIA_ROOT}/drivers/{old_email}',
                f'{settings.MEDIA_ROOT}/drivers/{instance.email}'
            )
            image = open(f'{settings.MEDIA_ROOT}/drivers/{instance.email}/avatars/{os.path.basename(old_user.image.name)}', 'rb')
            django_image = File(image)
            instance.image = django_image
            # instance.image = f'{settings.MEDIA_ROOT}/drivers/{instance.email}/avatars/{os.path.basename(old_user.image.name)}'
            os.remove(f'{settings.MEDIA_ROOT}/drivers/{instance.email}/avatars/{os.path.basename(old_user.image.name)}')

@receiver(post_save, sender=Car)
def post_save_cars(created, **kwargs):
    instance = kwargs['instance']
    if created:
        print(f"{instance.registration_number} создана!")

        # создание папки для машины
        os.mkdir(f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}')

        # создание папки для хранения аватарок
        os.mkdir(f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/avatars')

        # создание папки для хранения документов
        os.mkdir(f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/docs')

@receiver(pre_save, sender=Car)
def pre_save_car(instance, **kwargs):
    print(instance._state.adding)
    if not (instance._state.adding):
        old_registration_number = Car.objects.get(pk=instance.pk).registration_number
        if instance.registration_number != old_registration_number:
            os.renames(
                f'{settings.MEDIA_ROOT}/cars/{old_registration_number}',
                f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}'
            )
        print(f"{instance.registration_number=}")
        print(f"{old_registration_number=}")
