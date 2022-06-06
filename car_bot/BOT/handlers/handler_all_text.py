from datetime import time
from time import sleep

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
        # текущее меню
        self.menu_type = 'nots'
        # текущие заметки
        self.nots = Notifications.objects.all()
        # текущие заявки
        self.apps = Application.objects.first()
        # шаг в заметках/заявки
        self.step = 0

    def pressed_btn_menu(self, message):
        """
        Обрабатывает нажатие клавиши меню
        Создает смс "Главное меню"
        Генерирует разаметку Стартового меню
        """

        self.bot.send_message(
            message.chat.id,
            "Главное меню",
            reply_markup=self.keybords.set_start_menu(message)
        )

    # ******* ОСНОВНОЕ МЕНЮ ******* #
    def pressed_btn_nots(self, message):
        """
        Обрабатывает нажатие кнопки Уведомения
        type_menu = уведомления
        юсер = юсер_по_чат_id

        """

        self.menu_type = 'nots'

        self.user = MyUser.objects.get(chat_id=message.chat.id)
        self.nots = Notifications.objects.filter(recipient=self.user, active=True)

        if self.nots:
            not1 = self.nots[0]
            self.step = 1
            self.bot.send_message(
                message.chat.id,
                'активные уведомления',
                reply_markup=self.keybords.set_active_nots_btns(len(self.nots), self.step)
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
        else:
            self.bot.send_message(
                message.chat.id,
                'НЕТ НОВЫХ УВЕДОЛМЕНИЙ',
                reply_markup=self.keybords.set_active_nots_btns(len(self.nots), self.step)
            )

    def pressed_btn_about(self, message):
        """Обрабытывает нажатие кнопки О программе"""

        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.set_start_menu(message))

    def pressed_btn_apps(self, message):
        """Обрабатывает нажатие кнопки заявки"""

        self.menu_type = 'apps'
        self.bot.send_message(
            message.chat.id,
            'МЕНЮ: заявки',
            reply_markup=self.keybords.set_apps_menu()
        )

    # ******* ЗАЯВКИ ******* #
    def pressed_btn_new_apps(self, message):
        """Обрабатывает нажатие кнопки новые заявки"""

        self.user = MyUser.objects.get(chat_id=message.chat.id)

        self.apps = Application.objects.filter(engineer=self.user, is_active=True, status='OE')
        if self.apps:
            app1 = self.apps[0]
            self.step = 1

            self.bot.send_message(
                message.chat.id,
                "МЕНЮ: новые заявки",
                reply_markup=self.keybords.set_apps_control_btns(
                    app_step=self.step,
                    count_apps=len(self.apps)
                )
            )
            message_to_del = self.bot.send_message(
                message.chat.id,
                MESSAGES['applications'].format(
                    app1.id,
                    app1.car.registration_number,
                    app1.type,
                    app1.description,
                    app1.manager_descr,
                    app1.end_date,
                ),
                reply_markup=self.keybords.set_accept_new_app(app_id=app1.id)
            )
            self.message_id = message_to_del

        else:
            self.bot.send_message(
                message.chat.id,
                "У вас нет активных заявок!",
                reply_markup=self.keybords.set_start_menu()
            )

    def pressed_btn_active_apps(self, message):
        """Обрабатывает нажатие кнопки Активные заявки"""

        self.user = MyUser.objects.get(chat_id=message.chat.id)

        self.apps = Application.objects.filter(engineer=self.user, status='REP')
        if self.apps:

            applications = """
            ЗАЯВКА НОМЕР:           {}
            МАШИНА                  {}
            ТИП:                    {}
            ОПИСАНИЕ:               {}
            КОММЕНТАРИЙ МЕНЕДЖЕРА:  {}
            ВЫПОЛНИТЬ ДО:           {}
            """
            self.bot.send_message(
                message.chat.id,
                "АКТИВНЫЕ ЗАЯВКИ"
            )
            for app1 in self.apps:
                self.bot.send_message(
                    message.chat.id,
                    MESSAGES['applications'].format(
                        app1.id,
                        app1.car.registration_number,
                        app1.type,
                        app1.description,
                        app1.manager_descr,
                        app1.end_date,
                    ),
                    reply_markup=self.keybords.set_inline_complete_btn(app_id=app1.id)
                )


        else:
             self.bot.send_message(
                 message.chat.id,
                 "У вас нет активных заявок!",
                 reply_markup =self.keybords.set_start_menu(message)
             )

    def pressed_btn_old_apps(self, message):
        """Обрабатывает нажатие кнопки Выполненные заявки"""

        self.user = MyUser.objects.get(chat_id=message.chat.id)

        self.apps = Application.objects.filter(engineer=self.user, status='V')
        if self.apps:

            applications = """
                    ЗАЯВКА НОМЕР:           {}
                    МАШИНА                  {}
                    ТИП:                    {}
                    ОПИСАНИЕ:               {}
                    КОММЕНТАРИЙ МЕНЕДЖЕРА:  {}
                    ВЫПОЛНИТЬ ДО:           {}
                    """

            for app1 in self.apps:
                self.bot.send_message(
                    message.chat.id,
                    MESSAGES['applications'].format(
                        app1.id,
                        app1.car.registration_number,
                        app1.type,
                        app1.description,
                        app1.manager_descr,
                        app1.end_date,
                    ),
                    reply_markup=self.keybords.set_deactivate_app3(app_id=app1.id)
                )

    # ******* НОВЫЕ ЗАЯВКИ ******* #
    def pressed_btn_next_app(self, message):
        """Обработывает нажатие клавиши следующая НОВАЯ заявка"""
        print("ВЫЗВАН btn_next_app")

        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.delete_message(message.chat.id, message.message_id - 1)

        # if self.step != 1:
        self.bot.delete_message(message.chat.id, message.message_id - 2)

        if self.step != len(self.apps):
            self.step = self.step + 1
        else:
            self.step = 1

        if self.apps:
            app1 = self.apps[self.step-1]
            self.bot.send_message(
                message.chat.id,
                "СЛЕДУЮЩАЯ новая заявка",
                reply_markup=self.keybords.set_apps_control_btns(
                    app_step=self.step,
                    count_apps=len(self.apps)
                )
            )

            self.bot.send_message(
                message.chat.id,
                MESSAGES['applications'].format(
                    app1.id,
                    app1.car.registration_number,
                    app1.type,
                    app1.description,
                    app1.manager_descr,
                    app1.end_date,
                ),
                reply_markup=self.keybords.set_accept_new_app(app_id=app1.id)
            )

        else:
            self.bot.send_message(
                message.chat.id,
                "У вас нет активных заявок!",
                reply_markup=self.keybords.set_start_menu()
            )

    def pressed_btn_last_app(self, message):
        """Обработывает нажатие клавиши предыдущая НОВАЯ заявка"""

        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.delete_message(message.chat.id, message.message_id - 1)

        # if self.step != 1:
        self.bot.delete_message(message.chat.id, message.message_id - 2)

        if self.step != 1:
            self.step = self.step - 1
        else:
            self.step = len(self.apps)

        if self.apps:
            app1 = self.apps[self.step-1]

            self.bot.send_message(
                message.chat.id,
                "ПРЕДЫДУЩАЯ заявка",
                reply_markup=self.keybords.set_apps_control_btns(
                    app_step=self.step,
                    count_apps=len(self.apps)
                )
            )

            self.bot.send_message(
                message.chat.id,
                MESSAGES['applications'].format(
                    app1.id,
                    app1.car.registration_number,
                    app1.type,
                    app1.description,
                    app1.manager_descr,
                    app1.end_date,
                ),
                reply_markup=self.keybords.set_accept_new_app(app_id=app1.id)
            )

        else:
            self.bot.send_message(
                message.chat.id,
                "У вас нет активных заявок!",
                reply_markup=self.keybords.set_start_menu()
            )

    def pressed_inline_btn_start_repair(self, call, code):
        """
        Обрабатывает нажатие inline-кнопки Приступить к ремонту
        """

        # 1) выбраная заявка status = "REP"
        app_to_repair = Application.objects.get(pk=code)
        app_to_repair.status = 'REP'
        app_to_repair.save()

        self.bot.answer_callback_query(
            call.id,
            "Заявка принята в работу!"
        )

        # 2) self.step = 1
        self.step = 1
        # sleep(5)
        # 3) self.apps = Application.objects.filter(en=self.user, active=True)
        self.apps = Application.objects.filter(engineer=self.user, status="OE")
        self.bot.delete_message(call.message.chat.id, call.message.message_id)

        if self.apps:
            app1 = self.apps[0]
            self.step = 1

            self.bot.send_message(
                call.message.chat.id,
                "Оставшиеся новые заявки",
                reply_markup=self.keybords.set_apps_control_btns(
                    app_step=self.step,
                    count_apps=len(self.apps)
                )
            )

            self.bot.send_message(
                call.message.chat.id,
                MESSAGES['applications'].format(
                    app1.id,
                    app1.car.registration_number,
                    app1.type,
                    app1.description,
                    app1.manager_descr,
                    app1.end_date,
                ),
                reply_markup=self.keybords.set_accept_new_app(app_id=app1.id)
            )

        else:
            self.bot.send_message(
                call.message.chat.id,
                "У вас нет активных заявок!",
                reply_markup=self.keybords.set_start_menu(call.message)
            )

    # ******* АКТИВНЫЕ ЗАЯВКИ ******* #
    def pressed_inline_btn_complete_app(self, call, code):
        """
           Обрабатывает входящие запросы на нажатие inline-кнопки Выполнить заявку
        """
        print("YES!DEACTIVATE_BTN2")

        # 1) выбраная заявка status = "V"
        app_to_repair = Application.objects.get(pk=code)
        app_to_repair.status = 'V'
        app_to_repair.is_active = False
        app_to_repair.save()

        self.bot.answer_callback_query(
            call.id,
            "Заявка выполнена!"
        )

        # 2) self.step = 1
        self.step = 1
        # sleep(5)
        # 3) self.apps = Application.objects.filter(engineer=self.user, status="RED")
        self.apps = Application.objects.filter(engineer=self.user, status="RED")
        self.bot.delete_message(call.message.chat.id, call.message.message_id)

        # if self.apps:
        #     app1 = self.apps[0]
        #     self.step = 1
        #
        #     self.bot.send_message(
        #         call.message.chat.id,
        #         "Оставшиеся новые заявки",
        #         reply_markup=self.keybords.set_apps_control_btns(
        #             app_step=self.step,
        #             count_apps=len(self.apps)
        #         )
        #     )
        #
        #     self.bot.send_message(
        #         call.message.chat.id,
        #         MESSAGES['applications'].format(
        #             app1.id,
        #             app1.car.registration_number,
        #             app1.type,
        #             app1.description,
        #             app1.manager_descr,
        #             app1.end_date,
        #         ),
        #         reply_markup=self.keybords.set_accept_new_app(app_id=app1.id)
        #     )
        #
        # else:
        #     self.bot.send_message(
        #         call.message.chat.id,
        #         "У вас нет активных заявок!",
        #         reply_markup=self.keybords.set_start_btns(call.message)
        #     )

    def pressed_inline_btn_finalize_app(self, call, code):
        """
           Обрабатывает входящие запросы на нажатие inline-кнопки Доработать заявку
        """
        print("YES!DEACTIVATE_BTN2")

        # 1) выбраная заявка status = "REP"
        app_to_repair = Application.objects.get(pk=code)
        app_to_repair.status = 'REP'
        app_to_repair.is_active = True
        app_to_repair.save()

        self.bot.answer_callback_query(
            call.id,
            "Заявка возвращена на доработку!"
        )

        # 2) self.step = 1
        self.step = 1
        # sleep(5)
        # 3) self.apps = Application.objects.filter(engineer=self.user, status="RED")
        # self.apps = Application.objects.filter(engineer=self.user, status="RED")
        self.bot.delete_message(call.message.chat.id, call.message.message_id)

    # ******* УВЕДОМЛЕНИЯ ******* #

    def pressed_inline_btn_access_note(self, call, code):
        """
           Обрабатывает входящие запросы на нажатие inline-кнопки подтвердить уведомление
        """

        # 1) выбранное уведомление anotective=False
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

        if self.nots:
            not1 = self.nots[0]

            # 4) Отправка смс "первое уведомление"
            self.bot.send_message(
                call.message.chat.id,
                f'Уведомление № {not1.id}',
                reply_markup=self.keybords.set_active_nots_btns(len(self.nots), self.step)
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
        else:
            self.bot.send_message(
                call.message.chat.id,
                "У вас нет новых уведомлений",
                reply_markup=self.keybords.set_active_nots_btns(len(self.nots), self.step)

            )

    def pressed_btn_next_not(self, message):
        """Обработывает нажатие клавиши следующее уведомление"""
        # print(f"{self.step}")
        print("YES! NEXT NOT")
        # print(f"{self.nots.count}")

        if self.step != len(self.nots):
            self.step = self.step + 1
        else:
            self.step = 1

        not1 = list(self.nots)[self.step-1]
        self.bot.send_message(
            message.chat.id,
            f'Уведомление № {not1.id}',
            reply_markup=self.keybords.set_active_nots_btns(len(self.nots), self.step)
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
            reply_markup=self.keybords.set_active_nots_btns(len(self.nots), self.step)
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

    # ******* ПРОСМОТРЕННЫЕ УВЕДОМЛЕНИЯ ******* #

    def pressed_btn_old_nots(self, message):
        """Обрабатывает нажатие кнопки Просмотренные уведомления"""

        old_nots = Notifications.objects.filter(recipient=self.user, active=False)

        self.bot.send_message(
            message.chat.id,
            'Просмотренные уведомления ',
            reply_markup=self.keybords.set_start_menu(message)
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



    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # ********** основные кнопки ********** #
            print(f"{message.text=}")

            if message.text == 'уведомления':
                self.pressed_btn_nots(message)

            if message.text == 'Меню':
                self.pressed_btn_menu(message)

            if message.text == '>>':
                print(f"{self.menu_type=}")
                if self.menu_type == 'nots':
                    self.pressed_btn_next_not(message)
                elif self.menu_type == 'apps':
                    self.pressed_btn_next_app(message)
            if message.text == '<<':
                if self.menu_type == 'nots':
                    self.pressed_btn_last_not(message)
                elif self.menu_type == 'apps':
                    self.pressed_btn_last_app(message)

            if message.text == 'Просмотренные уведомления':
                self.pressed_btn_old_nots(message)

            if message.text == 'О программе':
                self.pressed_btn_about(message)


            # ******* механик ****** #

            if message.text == 'Заявки':
                self.pressed_btn_apps(message)

            if message.text == 'Новые заявки':
                self.pressed_btn_new_apps(message)

            if message.text == 'Активные заявки':
                self.pressed_btn_active_apps(message)

            if message.text == 'Выполненные заявки':
                self.pressed_btn_old_apps(message)
        #Обработчик нажатия инлайновых клавиш
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            inline_text = call.message.json['reply_markup']['inline_keyboard'][0][0]['text']
            # for key, value in call.message.json.items():
            #     print(key, ":", value)
            # print(call.message.json['reply_markup']['inline_keyboard'][0][0]['text'])
            # 'reply_markup': {'inline_keyboard': [[{'text': 'Приступить к ремонту',
            if code.isdigit():
                code = int(code)

            # ********  УВЕДМОЛЕНИЯ ******** #
            if inline_text == 'Подтвердить':
                self.pressed_inline_btn_access_note(call, code)

            # ********  ЗАЯВКИ ******** #

            if inline_text == 'Приступить к ремонту':
                self.pressed_inline_btn_start_repair(call, code)
            if inline_text == 'Выполнить заявку':
                self.pressed_inline_btn_complete_app(call, code)
            if inline_text == 'Доработать заявку':
                self.pressed_inline_btn_finalize_app(call, code)
