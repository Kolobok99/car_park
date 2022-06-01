# добавляем настройки
import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "car_park.settings") # project_name название проекта
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

    def entered_number(self, message):
        """
        обрабатывает входящие /start команды
        """

        users = MyUser.objects.all()
        number = message.text
        flag = False
        for user in users:
            if user.phone == number:
                self.bot.send_message(message.chat.id,
                                      f'{user.first_name}, авторизация прошла успешно',
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
        @self.bot.message_handler(content_types=["text"])
        def handle_text(message):
            self.entered_number(message)
