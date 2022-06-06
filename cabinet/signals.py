import os
import shutil
from datetime import timedelta

from django.core.files import File
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.conf import settings
from django.dispatch import Signal
from cabinet.models import MyUser, Car, FuelCard, Application

from simple_history.signals import (
    pre_create_historical_record,
    post_create_historical_record,
)

from car_bot.models import Notifications


# @receiver(pre_save, sender=Application)
# def pre_save_app(instance, **kwargs):
#     if instance._state.adding:
#         if instance.urgency == 'N':
#             instance.end_date = instance.start_date + timedelta(days=10)
#         elif instance.urgency == 'U':
#             instance.end_date = instance.start_date + timedelta(days=7)
#         elif instance.urgency == 'V':
#             instance.end_date = instance.start_date + timedelta(days=3)
#         # instance.save()

@receiver(post_save, sender=Notifications)
def post_save_nots(created, **kwargs):
    instance = kwargs['instance']
    if created:
        count = Notifications.objects.filter(recipient=instance.recipient).count()
        instance.owner_pk = Notifications.objects.filter(recipient=instance.recipient).count()
        instance.save()
@receiver(signal=post_save, sender=Application)
def post_save_apps(created, instance, **kwargs):
    manager = MyUser.objects.get(role='m')
    if created:
        if instance.urgency == 'N':
            instance.end_date = instance.start_date + timedelta(days=10)
        elif instance.urgency == 'U':
            instance.end_date = instance.start_date + timedelta(days=7)
        elif instance.urgency == 'V':
            instance.end_date = instance.start_date + timedelta(days=3)
        instance.save()
    #
    #     # Создана новая заявка
    #     if instance.status == 'O':
    #         if instance.owner != manager:
    #             Notifications.objects.create(
    #                 recipient=manager,
    #                 content=f"Заявка №{instance.pk}  ожидает рассмотрения",
    #                 content_object=instance
    #             )
    #     # Заявка направлена механику
    #     elif instance.status == 'OE':
    #         if instance.owner != manager:
    #             # Уведомление владельцу заявки
    #             Notifications.objects.create(
    #                 recipient=instance.owner,
    #                 content=f"Ваша заявка №{instance.pk} рассмотрена\n"
    #                         f"Комментарий менеджера: {instance.manager_descr}",
    #                 content_object=instance
    #             )
    #         # Уведомление механику
    #         Notifications.objects.create(
    #             recipient=instance.engineer,
    #             content=f"У вас новая заявка на ремонт {instance.pk}\n"
    #                     f"Комментарий менеджера: {instance.manager_descr}",
    #             content_object=instance
    #         )

    # Заявка направлена механику
    elif instance.status == 'OE':
        # Уведомление владельцу заявки
        if instance.owner != manager:
            Notifications.objects.create(
                recipient=instance.owner,
                content=f"Ваша заявка №{instance.pk} рассмотрена\n"
                        f"Комментарий менеджера: {instance.manager_descr}",
                content_object=instance
            )
        # Уведомление механику
        Notifications.objects.create(
            recipient=instance.engineer,
            content=f"У вас новая заявка на ремонт {instance.pk}\n"
                    f"Комментарий менеджера: {instance.manager_descr}",
            content_object=instance
        )
    # Механик приступил к работе
    elif instance.status == 'REP':
        # Уведомление менеджеру
        Notifications.objects.create(
            recipient=manager,
            content=f"Механик приступил к выполнению заявки № {instance.pk}",
            content_object=instance
        )
    # Механик выполнил заявку
    elif instance.status == 'V':
        # Уведомление менеджеру
        Notifications.objects.create(
            recipient=manager,
            content=f"Механик выполнил заявку № {instance.pk}",
            content_object=instance
        )

    elif instance.status == 'T':
        Notifications.objects.create(
            recipient=instance.owner,
            content=f"Ваша заявка №{instance.pk} ОТКЛОНЕНА!",
            content_object=instance
        )


@receiver(post_save, sender=MyUser)
def post_save_myuser(created, **kwargs):
    """Создает директорию для нового user'a"""
    instance = kwargs['instance']
    if created:
        #создание папки для пользователя
        os.mkdir(f'{settings.MEDIA_ROOT}/drivers/{instance.email}')
        #создание папки для хранения аватарок
        os.mkdir(f'{settings.MEDIA_ROOT}/drivers/{instance.email}/avatars')
        #создание папки для хранения документов
        os.mkdir(f'{settings.MEDIA_ROOT}/drivers/{instance.email}/docs')

@receiver(pre_save, sender=MyUser)
def pre_save_myuser(instance, **kwargs):
    """При изменении email'а, переименовывает личную директорию user'а """
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
    """Удаляет директорию удаляемого водителя"""
    try:
        user_dir = f"{settings.MEDIA_ROOT}/drivers/{instance.email}"
        shutil.rmtree(user_dir)
    except:
        pass



@receiver(post_save, sender=Car)
def post_save_cars(created, **kwargs):
    """Создает директорию для нового авто"""
    instance = kwargs['instance']
    if created:
        print(f"{instance.registration_number} создана!")
        # создание папки для машины
        os.mkdir(f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}')
        # создание папки для хранения аватарок
        os.mkdir(f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/avatars')
        # создание папки для хранения документов
        os.mkdir(f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/docs')

        # Если машина впервые добавляется
        if instance.owner:
            Notifications.objects.create(
                recipient=instance.owner,
                content=f"Вам присвоена новое авто ({instance.registration_number})",
                content_object=instance
            )

@receiver(pre_save, sender=Car)
def pre_save_car(instance, **kwargs):
    """При изменении регистрационного номера, переименовывает личную директорию авто"""
    instance.registration_number = instance.registration_number.upper()
    if not instance._state.adding:
        car = Car.objects.get(pk=instance.pk)
        old_registration_number = car.registration_number
        if instance.registration_number != old_registration_number:
            os.renames(
                f'{settings.MEDIA_ROOT}/cars/{old_registration_number}',
                f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}'
            )
            if car.image:
                # Переносим аватарку:
                avatar_path = f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/avatars/{os.path.basename(car.image.name)}'
                image = open(avatar_path, 'rb')
                django_image = File(image)
                instance.image = django_image
                os.remove(avatar_path)
            if car.my_docs.all():
                # Переносим документы
                pathes = [f'{settings.MEDIA_ROOT}/cars/{instance.registration_number}/docs/{os.path.basename(doc.file.name)}' for doc in car.my_docs.all()]
                files = [open(path, 'rb') for path in pathes]
                django_files = [File(file) for file in files]
                for id, obj in enumerate(instance.my_docs.all()):
                    obj.file = django_files[id]
                    obj.save()
                    os.remove(pathes[id])
        # При изменении водителя создает уведомление
        manager = MyUser.objects.get(role='m')
        old_owner = car.owner
        new_owner = instance.owner
        # 1) old_owner = None, new_owner = some_owner (добавление водителя)
        # 2) old_owner = some_owner, new_owner = some_owner_2 (изменение водителя)
        # 3) old_owner = some_owner, new_owner = None (удаление водителя)
        # 4) old_owner = None, new_owner = None (водитель не добавялется)
        # 5) old_owner = some_owner, new_owner = some_owner (водитель не изменяется)

        # 1) old_owner = None, new_owner = some_owner (добавление водителя)
        if old_owner is None and new_owner is not None:
            Notifications.objects.create(
                recipient=new_owner,
                content=f"Вам присвоена новое авто ({instance.registration_number})",
                content_object=instance
            )

        # 3) old_owner = some_owner, new_owner = None (удаление водителя)
        elif old_owner is not None and new_owner is None:
            Notifications.objects.create(
                recipient=old_owner,
                content=f"Ваша машина ({instance.registration_number}) изъята :-(",
                content_object=instance
            )


        # 2) old_owner = some_owner, new_owner = some_owner_2 (изменение водителя)
        elif old_owner != new_owner:
            Notifications.objects.create(
                recipient=old_owner,
                content=f"Ваша машина ({instance.registration_number}) изъята :-(",
                content_object=instance
            )

            Notifications.objects.create(
                recipient=new_owner,
                content=f"Вам присвоена новое авто ({instance.registration_number})",
                content_object=instance
            )




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
    """Удаляет директорию удаляемого авто"""
    car_dir = f"{settings.MEDIA_ROOT}/cars/{instance.registration_number}"
    shutil.rmtree(car_dir)

    if instance.owner:
        Notifications.objects.create(
            recipient=instance.owner,
            content=f"Ваша машина ({instance.registration_number}) УДАЛЕНА :-(",
            content_object=instance
        )

@receiver(post_save, sender=FuelCard)
def post_save(created, **kwargs):
    instance = kwargs['instance']
    if created:
        if instance.owner:
            Notifications.objects.create(
                recipient=instance.owner,
                content=f"Вам добавлена новая карта!",
                content_object=instance
            )


@receiver(pre_save, sender=FuelCard)
def pre_save_card(instance, **kwargs):
    """Создает уведомление об изъятии и присваивании карт"""
    if not instance._state.adding:
        old_owner = FuelCard.objects.get(pk=instance.pk).owner
        new_owner = instance.owner


        # 1) old_owner = None, new_owner = some_owner (присваивание карты)
        if old_owner is None and new_owner is not None:
            Notifications.objects.create(
                recipient=new_owner,
                content=f"Вам добавлена новая карта!",
                content_object=instance
            )
        # 2) old_owner = some_owner, new_owner = None (изъятие карты)
        elif old_owner and new_owner is None:
            Notifications.objects.create(
                recipient=old_owner,
                content=f"У вас изъята карта",
                content_object=instance
            )

@receiver(pre_delete, sender=FuelCard)
def pre_delete_card(instance, **kwargs):
    """Создает уведомление об удалении карты"""
    if instance.owner:
        Notifications.objects.create(
            recipient=instance.owner,
            content=f"Ваша карту УДАЛЕНА!",
            content_object=instance
        )
