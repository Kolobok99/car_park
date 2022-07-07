import pytest

from to_delete.early_pages import AccountPage
from to_delete.early_pages import RegistrationPage
from to_delete.early_pages import LoginPage

LINK = "/"
class TestLoginPage():

    @pytest.mark.skip
    def test_this_is_login_page(self, browser, live_server):
        """Тест: это стр. авторизации?"""
        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость проверяет, что он на стр. "авторизации"
        page.should_be_login_page()

    @pytest.mark.skip
    def test_quest_should_see_registration_link(self, browser, live_server):
        """Тест: наличие ссылки на стр. регистрации"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость проверяет, что он на стр. "Регистрации"
        page.should_be_registration_url()

    # @pytest.mark.skip
    @pytest.mark.new_test
    def test_quest_can_go_to_registration_page(self, browser, live_server):
        """Тест: возможность перехода на стр. регистрации"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость нажимает на кнопку "Регистрации
        page.go_to_registration_page()
        # Инициализация объекта "Регистрация"
        reg_page = RegistrationPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        reg_page.should_be_registration_page()

    @pytest.mark.xfail
    @pytest.mark.skip
    def test_quest_should_see_account_activation_link(self, browser, live_server):
        """Тест: наличие ссылки на стр. активации аккаунта"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость проверяет наличие ссылки для перехода
        # на стр. "Активации аккаунта"
        page.should_be_account_activation_link()

    @pytest.mark.skip
    def test_quest_can_go_to_account_activation_page(self, browser):
        """Тест: возможность перехода на стр. регистрации"""
        pass

    @pytest.mark.xfail
    @pytest.mark.skip
    def test_quest_should_see_password_change_link(self, browser, live_server):
        """Тест: наличие ссылки на стр. смены пароля"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость проверяет наличие ссылки для перехода
        # на стр. "Смены пароля"
        page.should_be_account_password_change_link()

    @pytest.mark.skip
    def test_guest_should_see_authorization_form(self, browser, live_server):
        """Тест: наличие формы авторизации"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость проверяет наличие формы авторизации
        page.should_be_authorization_form()

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_manager_can_authorization_with_valid_data(self, browser, create_user, live_server):
        """Тест: возможность залогиниться под валидными данными (менеджер) """
        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Менеджер переходит на стр. авторизации
        page.open()

        # Получаем данные формы авторизации
        authorization_form_dict = page.should_be_authorization_form()

        # Создаем тестового менеджера
        test_manager, password = create_user(role='m')

        # Менеджер вводит данные для входа и нажимает кнопку отправить
        page.user_login_with_valid_data(test_manager, password, authorization_form_dict)
        # Инициализация объекта "Аккаунт"
        account_page = AccountPage(browser, browser.current_url)

        # Менеджер проверяет, что он находится на стр. авторизации
        account_page.should_be_account_page()

    @pytest.mark.new_test
    def test_manager_cant_authorization_with_INvalid_email(self, browser, live_server):
        """Тест: возможность залогиниться под НЕвалидными данными """
        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Получаем данные формы авторизации
        authorization_form_dict = page.should_be_authorization_form()
        email = "fake@email.com"
        password = "12345"

        # Гость вводит невалидные данные и нажимает кнопку отправить
        page.guest_login_with_INvalid_data(email=email, password=password, form_data=authorization_form_dict)
        # Гость видит сообщение о вводе невалидных данных
        page.should_be_login_error()

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_driver_can_authorization_with_valid_data(self, browser, create_user, live_server):
        """Тест: возможность залогиниться под валидными данными (водитель)"""
        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Водитель переходит на стр. авторизации
        page.open()

        # Получаем данные формы авторизации
        authorization_form_dict = page.should_be_authorization_form()
        # Создаем тестового водителя
        test_driver, password = create_user(role='d')

        # Менеджер вводит данные для входа и нажимает кнопку отправить
        page.user_login_with_valid_data(test_driver, password, authorization_form_dict)
        # Инициализация объекта "Аккаунт"
        account_page = AccountPage(browser, browser.current_url)
        # Гость видит сообщение о вводе невалидных данных
        account_page.should_be_account_page()


    def guest_canT_open_account_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'account'"""
        pass

    def guest_canT_open_cars_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'cars'"""
        pass

    def guest_canT_open_drivers_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'drivers'"""
        pass
    def guest_canT_open_cards_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'cards'"""
        pass

    def guest_canT_open_applications_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'applications'"""
        pass

    def guest_canT_open_car_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'car/A111AA/'"""
        pass
    def guest_canT_open_app_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'app/1/'"""
        pass





