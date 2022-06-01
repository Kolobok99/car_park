# импортируем класс родитель
from telebot import types

from car_bot.BOT.handlers.handler import Handler


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        обрабатывает входящие /start команды
        """

        # Дублируем сообщением о том,
        # что пользователь сейчас отправит боту свой номер телефона

        self.bot.send_message(message.chat.id, 'Номер телефона',
                         reply_markup=self.keybords.set_send_number())


    def pressed_btn_number(self, message):
        """
        Обрабатывает входящие /number команды
        """
        self.bot.send_message(message.chat.id, f"Ваш номер: ")



    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие /start команды.
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)

        @self.bot.message_handler(commands=['number'])
        def handle(message):
            self.pressed_btn_number(message)