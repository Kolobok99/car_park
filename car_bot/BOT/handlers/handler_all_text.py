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


class HandlerAllText(Handler):
    """
    Класс обрабатывает события нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)

        #текущий юсер
        self.user = MyUser.objects.first()
        # текущие заметки
        self.nots = Notifications.objects.all()
        # шаг в заметках
        self.step = 0


    def pressed_btn_category(self, message):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точне
        это выбор категории товаров
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_info(self, message):
        """
        Обработка события нажатия на кнопку 'О магазине'
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        Обработка события нажатия на кнопку 'Настройки'
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        """
        Обработка события нажатия на кнопку 'Назад'
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_product(self, message, product):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точнее
        это выбор товара из категории
        """
        self.bot.send_message(message.chat.id, 'Категория ' +
                              config.KEYBOARD[product],
                              reply_markup=
                              self.keybords.set_select_category(
                                  config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Заказ'.
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step + 1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(
                                  product_id),
                                  self.BD.select_single_product_title(
                                      product_id),
                                  self.BD.select_single_product_price(
                                      product_id),
                                  self.BD.select_order_quantity(
                                      product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(
                                  self.step, quantity))

    def pressed_btn_up(self, message):
        """
        Обработка нажатия кнопки увеличения
        количества определенного товара в заказе
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции в пролуктов
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим изменения в БД orders
            self.BD.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_douwn(self, message):
        """
        Обработка нажатия кнопки уменьшения
        количества определенного товара в заказе
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции в пролуктов
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        # если товар в заказе есть
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим изменения в БД orders
            self.BD.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """
        Обработка нажатия кнопки удаления
        товарной позиции заказа
        """
        # получаем список всех product_id заказа
        count = self.BD.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:
            # получаем количество конкретной позиции в заказе
            quantity_order = self.BD.select_order_quantity(count[self.step])
            # получаем количество товара к конкретной
            # позиции заказа для возврата в product
            quantity_product = self.BD.select_single_product_quantity(
                count[self.step])
            quantity_product += quantity_order
            # вносим изменения в БД orders
            self.BD.delete_order(count[self.step])
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
            # уменьшаем шаг
            self.step -= 1

        count = self.BD.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:

            quantity_order = self.BD.select_order_quantity(count[self.step])
            # отправляем пользователю сообщение
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        """
        Обработка нажатия кнопки перемещения
        к более ранним товарным позициям заказа
        """
        # уменьшаем шаг пока шаг не будет равет "0"
        if self.step > 0:
            self.step -= 1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step],quantity,message)

    def pressed_btn_next_step(self, message):
        """
        Обработка нажатия кнопки перемещения
        к более поздним товарным позициям заказа
        """
        # увеличиваем шаг пока шаг не будет равет количеству строк
        # полей заказа с расчетом цены деления начиная с "0"
        if self.step < self.BD.count_rows_order()-1:
            self.step += 1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем еоличество конкретного товара в соответствие с шагом выборки
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apllay(self, message):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'Оформить заказ'.
        """
        # отправляем ответ пользователю
        self.bot.send_message(message.chat.id,
                              MESSAGES['applay'].format(
                                  utility.get_total_coas(self.BD),

                                  utility.get_total_quantity(self.BD)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.category_menu())
        # отчищаем данные с заказа
        self.BD.delete_all_order()

    def pressed_btn_nots(self, message):
        """Обрабатывает нажатие кнопки Уведомения"""

        self.user = MyUser.objects.get(chat_id=message.chat.id)
        self.nots = Notifications.objects.filter(recipient=self.user, active=True)
        not1 = self.nots[0]
        self.step = 1
        self.bot.send_message(
            message.chat.id,
            'активные уведомления',
            reply_markup=self.keybords.set_notifications_btns(len(self.nots), self.step)
        )

        self.bot.send_message(
            message.chat.id,
            MESSAGES['notifications'].format(
                not1.id,
                not1.created_at,
                not1.content
            ),
            reply_markup=self.keybords.set_deactivate_not(not_id=not1.id)
        )

    def pressed_btn_menu(self, message):
        """Обрабатывает нажатие клавиши меню"""

        self.bot.send_message(
            message.chat.id,
            "Меню",
            reply_markup=self.keybords.set_start_btns()
        )

    def pressed_btn_next_not(self, message):
        """Обработывает нажатие клавиши следующее уведомление"""
        # print(f"{self.step}")
        # print(f"{self.nots.count}")

        if self.step != len(self.nots):
            self.step = self.step + 1
        else:
            self.step = 1

        not1 = list(self.nots)[self.step-1]
        self.bot.send_message(
            message.chat.id,
            f'Уведомление № {not1.id}',
            reply_markup=self.keybords.set_notifications_btns(len(self.nots), self.step)
        )

        self.bot.send_message(
            message.chat.id,
            MESSAGES['notifications'].format(
                not1.id,
                not1.created_at,
                not1.content
            ),
            reply_markup=self.keybords.set_deactivate_not(not_id=not1.id)
        )

    def pressed_btn_last_not(self, message):
        """Обработывает нажатие клавиши предыдущее уведомление уведомление"""
        # print(f"{self.step}")
        # print(f"{self.nots.count}")

        if self.step != 1:
            self.step = self.step - 1
        else:
            self.step = len(self.nots)

        not1 = list(self.nots)[self.step-1]
        self.bot.send_message(
            message.chat.id,
            f'Уведомление № {not1.id}',
            reply_markup=self.keybords.set_notifications_btns(len(self.nots), self.step)
        )

        self.bot.send_message(
            message.chat.id,
            MESSAGES['notifications'].format(
                not1.id,
                not1.created_at,
                not1.content

            ),
            reply_markup=self.keybords.set_deactivate_not(not_id=not1.id)
        )

    def pressed_btn_deactivate_note(self, call, code):
        """
           Обрабатывает входящие запросы на нажатие inline-кнопки подтвердить заявку
        """

        # 1) выбранное уведомление active=False
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

        # 2) self.step = 1
        self.step = 1

        # 3) self.nots = Notifications.objects.filter(recipient=self.user, active=True)
        self.nots = Notifications.objects.filter(recipient=self.user, active=True)
        not1 = self.nots[0]

        # 4) Отправка смс "первое уведомление"
        self.bot.send_message(
            call.message.chat.id,
            f'Уведомление № {not1.id}',
            reply_markup=self.keybords.set_notifications_btns(len(self.nots), self.step)
        )
        # 5) Создание размекти кнопок



        self.bot.send_message(
            call.message.chat.id,
            MESSAGES['notifications'].format(
                not1.id,
                not1.created_at,
                not1.content
            ),
            reply_markup=self.keybords.set_deactivate_not(not_id=not1.id)
        )

    def pressed_btn_old_nots(self, message):
        """Обрабатывает нажатие кнопки Просмотренные уведомления"""

        old_nots = Notifications.objects.filter(recipient=self.user, active=False)

        self.bot.send_message(
            message.chat.id,
            'Просмотренные уведомления ',
            reply_markup=self.keybords.set_start_btns()
        )

        for not1 in old_nots:
            self.bot.send_message(
                message.chat.id,
                MESSAGES['notifications'].format(
                    not1.id,
                    not1.created_at,
                    not1.content
                ),
            )

    def pressed_btn_about(self, message):
        """Обрабытывает нажатие кнопки О программе"""

        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.set_start_btns())

    def pressed_btn_apps(self, message):
        """Обрабатывает нажатие кнопки заявки"""

        self.user = MyUser.objects.get(chat_id=message.chat.id)

        self.apps = Application.objects.filter(owner=self.user, active=True)
        not1 = self.nots[0]
        self.step = 1
        self.bot.send_message(
            message.chat.id,
            'активные уведомления',
            reply_markup=self.keybords.set_notifications_btns(len(self.nots), self.step)
        )

        self.bot.send_message(
            message.chat.id,
            MESSAGES['notifications'].format(
                not1.id,
                not1.created_at,
                not1.content
            ),
            reply_markup=self.keybords.set_deactivate_not(not_id=not1.id)
        )

        self.bot.send_message(
            message.chat.id,
            f"Активные заявки:"
        )



    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # ********** меню ********** #

            if message.text == 'уведомления':
                self.pressed_btn_nots(message)

            if message.text == 'Меню':
                self.pressed_btn_menu(message)

            if message.text == '>>':
                self.pressed_btn_next_not(message)

            if message.text == '<<':
                self.pressed_btn_last_not(message)

            if message.text == 'Просмотренные уведомления':
                self.pressed_btn_old_nots(message)

            if message.text == 'О программе':
                self.pressed_btn_about(message)


            # ******* механик ****** #

            if message.text == 'Заявки':
                self.pressed_btn_apps(message)

            # if message.text == config.KEYBOARD['CHOOSE_GOODS']:
            #     self.pressed_btn_category(message)
            #
            # if message.text == config.KEYBOARD['INFO']:
            #     self.pressed_btn_info(message)
            #
            # if message.text == config.KEYBOARD['SETTINGS']:
            #     self.pressed_btn_settings(message)
            #
            # if message.text == config.KEYBOARD['<<']:
            #     self.pressed_btn_back(message)
            #
            # if message.text == config.KEYBOARD['ORDER']:
            #     # если есть заказ
            #     if self.BD.count_rows_order() > 0:
            #         self.pressed_btn_order(message)
            #     else:
            #         self.bot.send_message(message.chat.id,
            #                               MESSAGES['no_orders'],
            #                               parse_mode="HTML",
            #                               reply_markup=self.keybords.
            #                               category_menu())
            #
            #
            # # ********** меню (категории товара, ПФ, Бакалея, Мороженое)******
            # if message.text == config.KEYBOARD['SEMIPRODUCT']:
            #     self.pressed_btn_product(message, 'SEMIPRODUCT')
            #
            # if message.text == config.KEYBOARD['GROCERY']:
            #     self.pressed_btn_product(message, 'GROCERY')
            #
            # if message.text == config.KEYBOARD['ICE_CREAM']:
            #     self.pressed_btn_product(message, 'ICE_CREAM')
            #
            #     # ********** меню (Заказа)**********
            #
            # if message.text == config.KEYBOARD['UP']:
            #     self.pressed_btn_up(message)
            #
            # if message.text == config.KEYBOARD['DOUWN']:
            #     self.pressed_btn_douwn(message)
            #
            # if message.text == config.KEYBOARD['X']:
            #     self.pressed_btn_x(message)
            #
            # if message.text == config.KEYBOARD['BACK_STEP']:
            #     self.pressed_btn_back_step(message)
            #
            # if message.text == config.KEYBOARD['NEXT_STEP']:
            #     self.pressed_btn_next_step(message)
            #
            # if message.text == config.KEYBOARD['APPLAY']:
            #     self.pressed_btn_apllay(message)
            #     # иные нажатия и ввод данных пользователем
            # else:
            #     self.bot.send_message(message.chat.id, message.text)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
                self.pressed_btn_deactivate_note(call, code)