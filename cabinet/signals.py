import os
import shutil

from django.core.files import File
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
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
        user = MyUser.objects.get(pk=instance.pk)
        old_email = user.email
        if instance.email != old_email:
            os.renames(
                f'{settings.MEDIA_ROOT}/drivers/{old_email}',
                f'{settings.MEDIA_ROOT}/drivers/{instance.email}'
            )
            #Переносим аватарку:
            avatar_path = f'{settings.MEDIA_ROOT}/drivers/{instance.email}/avatars/{os.path.basename(user.image.name)}'
            image = open(avatar_path, 'rb')
            django_image = File(image)
            instance.image = django_image
            os.remove(avatar_path)

            #Переносим документы
            pathes = [f'{settings.MEDIA_ROOT}/drivers/{instance.email}/docs/{os.path.basename(doc.file.name)}' for doc in user.my_docs.all()]
            files = [open(path, 'rb') for path in pathes]
            django_files = [File(file) for file in files]
            for id, obj in enumerate(instance.my_docs.all()):
                obj.file = django_files[id]
                obj.save()
                os.remove(pathes[id])

@receiver(pre_delete, sender=MyUser)
def pre_delete_car(instance, **kwargs):
    user_dir = f"{settings.MEDIA_ROOT}/drivers/{instance.email}"
    shutil.rmtree(user_dir)


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
    print(f"asdsada {instance._state.adding=}")
    instance.registration_number = instance.registration_number.upper()
    if not instance._state.adding:
        car = Car.objects.get(pk=instance.pk)
        old_registration_number = car.registration_number
        if instance.registration_number != old_registration_number:
            os.renames(
                f'{settings.MEDIA_ROOT}/cars/{old_registration_number}',
                f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}'
            )
            # Переносим аватарку:
            avatar_path = f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/avatars/{os.path.basename(car.image.name)}'
            image = open(avatar_path, 'rb')
            django_image = File(image)
            instance.image = django_image
            os.remove(avatar_path)

            # Переносим документы
            pathes = [f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/docs/{os.path.basename(doc.file.name)}' for doc in car.my_docs.all()]
            files = [open(path, 'rb') for path in pathes]
            django_files = [File(file) for file in files]
            for id, obj in enumerate(instance.my_docs.all()):
                obj.file = django_files[id]
                obj.save()
                os.remove(pathes[id])

            # pathes = [f'{settings.MEDIA_ROOT}/drivers/{instance.email}/docs/{os.path.basename(doc.file.name)}' for doc
            #           in user.my_docs.all()]
            # files = [open(path, 'rb') for path in pathes]
            # django_files = [File(file) for file in files]
            # for id, obj in enumerate(instance.my_docs.all()):
            #     obj.file = django_files[id]
            #     obj.save()
            #     os.remove(pathes[id])

@receiver(pre_delete, sender=Car)
def pre_delete_car(instance, **kwargs):
    car_dir = f"{settings.MEDIA_ROOT}/cars/{instance.registration_number}"
    shutil.rmtree(car_dir)