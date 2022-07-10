from car_bot.BOT.handlers.handler_all_text import HandlerAllText
# from to_delete.handler_content_types import HandlerContentTypes
from car_bot.BOT.handlers.handler_com import HandlerCommands


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        # получаем бота
        self.bot = bot
        # иницаилизация обработчиков
        self.handler_commands = HandlerCommands(self.bot)
        # self.handler_contypes = HandlerContentTypes(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)

    def handle(self):
        # запуск обработчиков
        self.handler_commands.handle()
        # self.handler_contypes.handle()
        self.handler_all_text.handle()
