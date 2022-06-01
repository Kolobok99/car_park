from car_bot.BOT.handlers.handler_com import HandlerCommands
from car_bot.BOT.handlers.handler_content_types import HandlerContentTypes


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot
        # здесь будет иницаилизация обработчиков
        self.handler_commands = HandlerCommands(self.bot)
        self.handler_contypes = HandlerContentTypes(self.bot)

    def handle(self):
        # здесь будет запуск обработчиков
        self.handler_commands.handle()
        self.handler_contypes.handle()
