# импортируем класс родитель

# Загушка для использования ORM
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")
django.setup()

from cabinet.models import MyUser
from car_bot.BOT.handlers.handler import Handler


class HandlerCommands(Handler):
    """
    обрабатывает входящие команды /start и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)
        self.user = MyUser.objects.first()

    def pressed_btn_start(self, message):
        """
        обрабатывает входящую /start команду
        """

        # Просим пользователя предоставить доступ к номеру телефона
        # и создаем соответсвующую кнопку
        self.bot.send_message(message.chat.id, 'Пожалуйста, предоставьте боту доступ к вашему номеру телефона',
                              reply_markup=self.keybords.set_send_number_btn())



    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие /start команды.
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
