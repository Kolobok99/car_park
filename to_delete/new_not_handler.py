import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")
django.setup()

from car_bot.models import Notifications
# импортируем ответ пользователю
from car_bot.BOT.settings.message import MESSAGES
from cabinet.models import MyUser, Application
from car_bot.BOT.settings import config
# импортируем класс-родитель
from car_bot.BOT.handlers.handler import Handler


class HandlerNewNote(Handler):
    """
    Класс обрабатывает события нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)

        #текущий юсер
        self.user = MyUser.objects.first()
        # текущее меню
        self.menu_type = 'nots'
        # текущие заметки
        self.nots = Notifications.objects.all()
        # текущие заявки
        self.apps = Application.objects.first()
        # шаг в заметках/заявки
        self.step = 0

