import django
import os

from car_bot.models import Notifications

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")
django.setup()


# импортируем класс родитель
from car_bot.BOT.handlers.handler import Handler
# импортируем сообщения пользователю
from car_bot.BOT.settings.message import MESSAGES


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлайн-кнопоки
    """

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_product(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие inline-кнопок товара
        """
        # создаем запись в БД по факту заказа
        self.BD._add_orders(1, code, 1)

        self.bot.answer_callback_query(
            call.id,
            MESSAGES['product_order'].format(
                self.BD.select_single_product_name(code),
                self.BD.select_single_product_title(code),
                self.BD.select_single_product_price(code),
                self.BD.select_single_product_quantity(code)),
            show_alert=True)

    def pressed_btn_deactivate_note(self, call, code):
        """
           Обрабатывает входящие запросы на нажатие inline-кнопки подтвердить заявку
        """

        not_to_deactivate = Notifications.objects.get(pk=code)
        not_to_deactivate.active = False
        not_to_deactivate.save()

        self.bot.answer_callback_query(
            call.id,
            MESSAGES['notifications'].format(
                not_to_deactivate.id,
                not_to_deactivate.created_at,
                not_to_deactivate.content,
            ))
        # self.bot.send_message(
        #     call.id,
        #
        # )

    def handle(self):
        # обработчик(декоратор) запросов от нажатия на кнопки товара.
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
                self.pressed_btn_deactivate_note(call, code)
