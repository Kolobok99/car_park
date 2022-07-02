from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from cabinet.models import MyUser


class Notifications(models.Model):
    """
        Модель: уведомлений, присылаемых ботом
    """

    recipient = models.ForeignKey(MyUser, verbose_name='получатель',
                                  on_delete=models.SET(1),
                                  related_name='received_nots')

    created_at = models.DateTimeField('Дата', auto_now_add=True)
    active = models.BooleanField('Активность', default=True)

    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.SET(1))

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',
                                       fk_field='object_id',)

    owner_pk = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'