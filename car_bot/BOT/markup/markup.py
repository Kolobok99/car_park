# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# импортируем настройки и утилиты
from car_bot.BOT.settings import config

# инициализируем настройки джанго для работы с БД
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")
django.setup()

from cabinet.models import MyUser


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """
    # инициализация разметки

    def __init__(self):
        self.markup = None

    def set_send_number_btn(self):
        """Создает кнопку отправки телефона"""

        # Подключаем клавиатуру
        self.markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        # Указываем название кнопки, которая появится у пользователя
        phone_btn = KeyboardButton(text="Отправить телефон", request_contact=True)

        # Добавляем эту кнопку
        self.markup.add(phone_btn)

        return self.markup

    def set_start_menu(self, message):
        """Создает разметку кнопок стартового меню"""
        user = MyUser.objects.get(chat_id=message.chat.id)
        self.markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        nots_btn = KeyboardButton(text="Уведомления")
        about_btn = KeyboardButton(text="О программе")

        self.markup.add(nots_btn, about_btn)

        if user.role == 'e':
            apps_btn = KeyboardButton(text='Заявки')
            self.markup.add(apps_btn)

        return self.markup

    def set_deactivate_not(self, not_id):
        """Создает кнопку подтверждения уведомления"""

        self.markup = InlineKeyboardMarkup(row_width=1)

        deactivate_btn = InlineKeyboardButton("Подтвердить", callback_data=not_id)

        self.markup.add(deactivate_btn)

        return self.markup

    def set_active_nots_btns(self, count_nots, not_step):
        """Создает разметку кнопок для работы с АКТИВНЫМИ уведомлениями"""

        self.markup = ReplyKeyboardMarkup(True, True)

        next_not_btn = KeyboardButton(text=">>")
        last_not_btn = KeyboardButton(text="<<")
        counter_nots_btn = KeyboardButton(text=f"{not_step} из {count_nots}")
        main_menu_btn = KeyboardButton(text="Меню")
        old_notes = KeyboardButton(text='Просмотренные уведомления')

        if count_nots:
            self.markup.add(last_not_btn, counter_nots_btn, next_not_btn)

        self.markup.add(old_notes, main_menu_btn)

        return self.markup

    def set_apps_menu(self):
        """Создает разметку кнопок меню Заявки"""

        self.markup = ReplyKeyboardMarkup(True, True)
        new_apps_btn = KeyboardButton(text="Новые заявки")
        active_apps_btn = KeyboardButton(text="Активные заявки")
        old_apps_btn = KeyboardButton(text="Выполненные заявки")
        menu_btn = KeyboardButton(text="Меню")

        self.markup.add(new_apps_btn, active_apps_btn)
        self.markup.add(old_apps_btn, menu_btn)

        return self.markup

    def set_deactivate_app(self, app_id):
        """Создает инлайновую кнопку деактивации Заявки"""

        self.markup = InlineKeyboardMarkup(row_width=1)
        deactivate_btn = InlineKeyboardButton("Подтвердить", callback_data=app_id)

        self.markup.add(deactivate_btn)

        return self.markup

    def set_inline_complete_btn(self, app_id):
        """Создает инлайновую кнопку для выполнения заявок"""

        self.markup = InlineKeyboardMarkup(row_width=1)
        deactivate2_btn = InlineKeyboardButton("Выполнить заявку", callback_data=app_id)

        self.markup.add(deactivate2_btn)

        return self.markup

    def set_deactivate_app3(self, app_id):
        """Создает инлайновую кнопку для выполнения заявок"""

        self.markup = InlineKeyboardMarkup(row_width=1)
        deactivate3_btn = InlineKeyboardButton("Доработать заявку", callback_data=app_id)

        self.markup.add(deactivate3_btn)

        return self.markup

    def set_apps_control_btns(self, app_step, count_apps):
        """Создает разметку кнопок для управления заявками"""

        self.markup = ReplyKeyboardMarkup(True, True)

        next_app_btn = KeyboardButton(text=">>")
        last_app_btn = KeyboardButton(text="<<")
        counter_apps_btn = KeyboardButton(text=f"{app_step} из {count_apps}")
        main_menu_btn = KeyboardButton(text="Меню")
        all_apps = KeyboardButton(text='Заявки')

        self.markup.add(last_app_btn, counter_apps_btn, next_app_btn)
        self.markup.add(all_apps, main_menu_btn)

        return self.markup

    def set_accept_new_app(self, app_id):
        """Создает разметку кнопок: принять и управление новыми заявками"""

        self.markup = InlineKeyboardMarkup(row_width=1)
        deactivate_btn = InlineKeyboardButton("Приступить к ремонту", callback_data=app_id)
        self.markup.add(deactivate_btn)

        return self.markup