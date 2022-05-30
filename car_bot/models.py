from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from cabinet.models import MyUser


class Notifications(models.Model):
    """
        Модель: уведомлений, присылаемых ботом
    """

    creator = models.ForeignKey(MyUser, verbose_name='создатель',
                                on_delete=models.SET(1),
                                null=True, blank=True, related_name='my_nots')
    recipient = models.ForeignKey(MyUser, verbose_name='получатель',
                                  on_delete=models.SET(1),
                                  related_name='received_nots')

    created_at = models.DateTimeField('Дата', auto_now_add=True)

    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',
                                       fk_field='object_id')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'