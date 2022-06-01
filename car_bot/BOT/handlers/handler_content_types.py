# добавляем настройки
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")
django.setup()

from cabinet.models import MyUser

# импортируем класс родитель
from car_bot.BOT.handlers.handler import Handler


class HandlerContentTypes(Handler):
    """
    Класс обрабатывает входящие команды /start и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def received_phone(self, message):
        """
        обрабатывает входящие /start команды
        """

        users = MyUser.objects.all()


        number = message.contact.phone_number
        flag = False
        for user in users:
            if user.phone[1:] == number[2:]:
                user.chat_id = message.chat.id
                user.save()
                self.bot.send_message(message.chat.id,
                                      f'{user.first_name}, авторизация прошла успешно',
                                      reply_markup=self.keybords.set_notifications()
                                      )
                flag = True
                break
        if not flag:
            self.bot.send_message(message.chat.id,
                                  f'Ваш номер не найден',
                                  )


    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие /start команды.
        @self.bot.message_handler(content_types=['contact'])
        def handle(message):
            self.received_phone(message)
