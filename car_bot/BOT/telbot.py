# импортируем функцию создания объекта бота
# from django.conf import settings
import time

from telebot import TeleBot
# импортируем основные настройки проекта
from car_bot.BOT.settings import config
# импортируем главный класс-обработчик бота
from car_bot.BOT.handlers.handler_main import HandlerMain


class TelBot:
    """
    Основной класс телеграмм бота (сервер), в основе которого
    используется библиотека pyTelegramBotAPI
    """
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        """
        Инициализация бота
        """
        # получаем токен
        self.token = config.TOKEN
        # инициализируем бот на основе зарегистрированного токена
        self.bot = TeleBot(self.token)
        # инициализируем оброботчик событий
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        Метод предназначен для старта обработчика событий
        """
        self.handler.handle()
        # pass
    def run_bot(self):
        """
        Метод запускает основные события сервера
        """
        # обработчик событий
        self.start()
        print("Обработчик событий запущен")
        # служит для запуска бота (работа в режиме нон-стоп)
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    while True:
        try:
            bot = TelBot()
            bot.run_bot()

        except Exception as e:
            print(e)  # или просто print(e) если у вас логгера нет,
            # или import traceback; traceback.print_exc() для печати полной инфы
            # time.sleep(15)

