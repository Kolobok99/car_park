import time

import pytest

from cabinet.models import MyUser, CarBrand, FuelCard, DocType
from cabinet.tests.end2end.pages.account_page import AccountPage
# from cabinet.early_tests.end2end.pages.new_cars_page import CarsPage
from cabinet.tests.end2end.pages.cars_page import CarsPage
from cabinet.tests.end2end.pages.reg_page import RegistrationPage
from cabinet.tests.end2end.pages.login_page import LoginPage
from car_park.settings import BASE_DIR

LINK = "/account/"
class TestAccountPage:


    def manager_login(self, browser, live_server, create_user):
        """Инициализация объекта 'Аккаунт (авторизация менеджера)'"""
        page = LoginPage(browser, live_server.url)
        page.open()
        login_form = page.should_be_sign_in_form()
        test_manager, manager_pass = create_user(role='m')
        login_data = {
            'FORM_LOGIN_INPUT_EMAIL': test_manager.email,
            'FORM_LOGIN_INPUT_PASSWORD': manager_pass,
        }
        page.user_sign_in(login_data, login_form)

        account_page = AccountPage(browser, browser.current_url)

        return account_page

    def test_this_is_account_page(self, browser, live_server, create_user):
        """Тест: это стр. ЛК?"""

        page = self.manager_login(browser, live_server, create_user)
        page.should_be_account_page()


     # -------- МЕНЕДЖЕР ----- #

    def test_manager_can_logount(self, browser, live_server, create_user):
        """Тест: менеджер может выйти из ЛК"""
        page = self.manager_login(browser, live_server, create_user)
        page.logout()
        login_page = LoginPage(browser, browser.current_url)
        login_page.guest_canT_go_to_cars_pages(live_server)

    def test_manager_can_go_to_cars_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'cars'"""
        page = self.manager_login(browser, live_server, create_user)
        # Гость нажимает на кнопку "Регистрации
        page.go_to_cars_page_by_btn()
        # Инициализация объекта "Регистрация"
        cars_page = CarsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        cars_page.should_be_cars_page()

    def test_manager_can_go_to_drivers_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'drivers'"""
        pass

    def test_manager_can_go_to_documents_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'documents'"""
        pass

    def test_manager_can_go_to_cards_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'cards'"""
        pass

    def test_manager_can_go_to_applications_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'applications'"""
        pass

    def test_manager_see_form_to_change_personal_data(self, browser, live_server, create_user):
        """Тест: менеджер видит форму изменения личных данных"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_form_to_change_data()

    def test_manager_can_change_personal_data_by_valid_data(self, browser, live_server, create_user):
        """Тест: менеджер может изменить личные данные (валидными данными)"""
        # Инициализируем объект 'Аккаунт'
        page = self.manager_login(browser, live_server, create_user)
        # Получаем форму смены персональных данных
        change_form = page.should_be_form_to_change_data()

        # Инициализация новых персональных данных
        change_data = {
            'FORM_PERSONAL_INPUT_F_NAME': 'Игнатий',
            'FORM_PERSONAL_INPUT_L_NAME': 'Лужков',
            'FORM_PERSONAL_INPUT_P_NAME': 'Петрович',
            'FORM_PERSONAL_INPUT_PHONE': '89324316789',
        }
        # Гость очищает поля формы
        page.clean_form(change_form)

        # Гость вводит данные, нажимает кнопку "Изменить данные"
        page.change_personal_data(change_data, change_form)

        # Менеджер видит сообщение 'Данные изменены!' и нажимает крестик
        page.close_change_personal_data_success_message()
        # time.sleep(20)
        page.check_personal_data(change_data)


    def test_manager_see_cars_table(self, browser, live_server, create_user):
        """Менеджер проверяет наличие таблицы 'машины'"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cars_table()

    def test_manager_see_apps_table(self, browser, live_server, create_user):
        """Менеджер проверяет наличие таблицы 'заявки'"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_apps_table()
    def test_manager_see_cards_table(self, browser, live_server, create_user):
        """Менеджер проверяет наличие таблицы 'топливные карты'"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cards_table()
    def test_manager_see_docs_table(self, browser, live_server, create_user):
        """Менеджер проверяет наличие таблицы 'документы'"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_docs_table()

    @pytest.mark.django_db
    def test_manager_can_change_card_balance(self, browser, live_server, create_user):
        """Тест: изменение баланса карты"""

        # Инициализируем объект 'Аккаунт'
        page = self.manager_login(browser, live_server, create_user)

        # Получаем тестового менеджера
        test_manager = MyUser.objects.get(email='test_manager@mail.com')

        # Добавляем менеджеру карту
        manager_card = FuelCard.objects.create(
            number='1234123412341234',
            limit=500,
            owner=test_manager,
        )
        page.reload()

        # Проверяем наличие карты в ЛК менеджера
        page.should_be_user_card(manager_card.pk)

        # Получаем форму "изменения баланса"
        change_balance_form = page.should_be_form_to_change_balance()
        card_balance_dict = {
            'FORM_CARD_BALANCE_INPUT_BALANCE': "200"
        }
        # Очищаем форму
        page.clean_form(change_balance_form)

        # Изменяем баланс
        page.change_card_balance(card_balance_dict, change_balance_form)

        # Проверяем баланс
        page.check_balance("200")

        # Закрываем сообщение об изменении баланса
        page.close_change_balance_msg()

    def test_manager_canT_change_card_INvalid_balance(self, browser, live_server, create_user):
        """Тест: изменение баланса карты на баланс превышающий лимит"""


        # Инициализируем объект 'Аккаунт'
        page = self.manager_login(browser, live_server, create_user)

        # Получаем тестового менеджера
        test_manager = MyUser.objects.get(email='test_manager@mail.com')

        # Добавляем менеджеру карту
        manager_card = FuelCard.objects.create(
            number='1234123412341234',
            limit=500,
            owner=test_manager,
        )
        page.reload()

        # Проверяем наличие карты в ЛК менеджера
        page.should_be_user_card(manager_card.pk)

        # Получаем форму "изменения баланса"
        change_balance_form = page.should_be_form_to_change_balance()
        card_balance_dict = {
            'FORM_CARD_BALANCE_INPUT_BALANCE': "700"
        }
        page.change_card_balance("700")

        # Проверяем баланс
        page.change_card_balance("500")


    def test_manager_can_add_doc_with_valid_data(self, browser, live_server,create_user):
        """Тест: возможность добавления корректного документа"""
        # Инициализируем объект 'Аккаунт'
        page = self.manager_login(browser, live_server, create_user)
        # Добавляем тип документа
        passport = DocType.objects.create(
            type='m',
            title='паспорт'
        )
        # Получаем форму добавления документа
        add_doc_form = page.should_be_doc_add_form()
        test_doc_path = str(BASE_DIR) + '/cabinet/early_tests/test_files/Instruction.pdf'
        doc_dict = {
            'FORM_DOC_ADD_INPUT_START_DATE': '10-10-2021',
            'FORM_DOC_ADD_INPUT_END_DATE': '21-12-2022',
            'FORM_DOC_ADD_INPUT_COPY': test_doc_path

        }
        # Открываем форму добавления документа,
        # заполняем ее нажимаем кнопку отправить
        page.add_doc(doc_dict, add_doc_form)

        # Форма исчезла
        page.add_doc_form_is_hide()

        # Закрываем сообщение "Документ добавлен!"
        page.close_message_add_doc_success()
        # Проверяем, что появился документ
        page.is_doc_in_table('паспорт', doc_dict['FORM_DOC_ADD_INPUT_START_DATE'], doc_dict['FORM_DOC_ADD_INPUT_END_DATE'])
        # Удаляем документ
        page.delete_doc(1)
        # Закрываем сообщение "Документ успешно удален!"
        page.close_message_delete_doc_success()


    def test_manager_canT_add_doc_with_INvalid_data(self, browser, live_server,create_user):
        """Тест: возможность добавления документа с НЕкорректной датой"""
        # Инициализируем объект 'Аккаунт'
        page = self.manager_login(browser, live_server, create_user)
        # Добавляем тип документа
        passport = DocType.objects.create(
            type='m',
            title='паспорт'
        )
        # Получаем форму добавления документа
        add_doc_form = page.should_be_doc_add_form()

        doc_dict = {
            'end_date': '10-10-2021',
            'start_date': '21-12-2022',

        }

        # page.add_user_doc(doc_dict, add_doc_form)
        # Открываем форму добавления документа,
        # заполняем ее нажимаем кнопку отправить
        page.add_doc(doc_dict, add_doc_form)

        # Проверяем, что форма появилась
        page.add_doc_form_is_NOT_hide()
        # Проверяем, что появилось сообщение об ошибке
        page.has_error()
        # Проверяем, что документ не добавился
     # -------- ВОДИТЕЛЬ ----- #

    def driver_can_logount(self, browser, live_server):
        """Тест: водитель может выйти из ЛК"""
        pass
    def test_driver_canT_go_to_cars_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'cars'"""
        pass

    def test_driver_canT_go_to_drivers_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'drivers'"""
        pass

    def test_driver_canT_go_to_documents_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'documents'"""
        pass

    def test_driver_canT_go_to_cards_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'cards'"""
        pass

    def test_driver_canT_go_to_applications_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'applications'"""
        pass

    def test_driver_can_see_form_to_change_personal_data(self, browser, live_server):
        """Тест: менеджер видит форму изменения личных данных"""
        pass

    def test_driver_can_change_personal_data_by_valid_data(self, browser, live_server):
        """Тест: водитель может изменить личные данные (валидными данными)"""
        pass

    def test_driver_see_cars_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'машины' """
        pass
    def test_driver_see_applications_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'заявки' """
        pass
    def test_driver_see_cards_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'топливные карты' """
        pass
    def test_driver_see_docs_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'документы' """
        pass

    def test_driver_can_add_doc(self, browser, live_server):
        """Тест: водитель может добавить документ """
        pass

    def test_driver_canT_add_doc_with_invalid_date(self, browser, live_server):
        """Тест: водитель НЕ может добавить новый документ с невалидной почтой"""
        pass
