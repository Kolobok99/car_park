import time
from unittest import TestCase

import pytest

from cabinet.models import MyUser, CarBrand
from cabinet.tests.end2end.new_pages.new_acc_activat_page import AccountActivationPage
from cabinet.tests.end2end.new_pages.new_locators import LoginPageLocators
from cabinet.tests.end2end.new_pages.new_pass_change_page import PasswordChange
from cabinet.tests.end2end.new_pages.new_account_page import AccountPage
from cabinet.tests.end2end.new_pages.new_reg_page import RegistrationPage
from cabinet.tests.end2end.new_pages.new_login_page import LoginPage

LINK = "/"
class TestLoginPage():

    # @pytest.mark.skip
    def test_this_is_login_page(self, browser, live_server):
        """Тест: это стр. авторизации?"""
        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()
        # Гость проверяет, что он на стр. "авторизации"
        page.should_be__page('')


    # @pytest.mark.skip
    # @pytest.mark.new_test
    def test_quest_can_go_to_registration_page(self, browser, live_server):
        """Тест: возможность перехода на стр. регистрации"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость нажимает на кнопку "Регистрация"
        page.go_to_registration_page_by_href()
        # Инициализация объекта "Регистрация"
        reg_page = RegistrationPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        reg_page.should_be__page('/registration/')

    @pytest.mark.xfail
    def test_quest_can_go_to_password_change_page(self, browser, live_server):
        """Тест: возможность перехода на стр. регистрации"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость нажимает на кнопку "Регистрация"
        page.go_to__page_by_href_btn(LoginPageLocators.PASSWORD_CHANGE_LINK, 'смена пароля')
        # Инициализация объекта "Регистрация"
        pass_change_page = PasswordChange(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        pass_change_page.should_be__page('/change-password/')

    @pytest.mark.xfail
    def test_quest_can_go_to_account_activation_page(self, browser, live_server):
        """Тест: возможность перехода на стр. регистрации"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость нажимает на кнопку "Активация аккаунта"
        page.go_to__page_by_href_btn(LoginPageLocators.ACC_ACTIVATION_LINK, 'активация аккаунта')
        # Инициализация объекта "Регистрация"
        pass_change_page = AccountActivationPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        pass_change_page.should_be__page('/acc-activation/')

    # @pytest.mark.skip
    def test_guest_can_see_authorization_form(self, browser, live_server):
        """Тест: наличие формы авторизации"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()
        # Гость проверяет наличие формы авторизации
        page.should_be_sign_in_form()

    @pytest.mark.django_db
    def test_manager_can_authorization_with_valid_data(self, browser, create_user, live_server):
        """Тест: возможность залогиниться под валидными данными (менеджер) """
        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Менеджер переходит на стр. авторизации
        page.open()

        # Получаем форму авторизации
        authorization_form_dict = page.should_be_sign_in_form()

        # Создаем тестового менеджера
        test_manager, password = create_user(role='m')

        # Менеджер вводит данные для входа и нажимает кнопку отправить
        page.user_sign_in(test_manager.email, password, authorization_form_dict)
        # Инициализация объекта "Аккаунт"
        account_page = AccountPage(browser, browser.current_url)

        # Менеджер проверяет, что он находится на стр. авторизации
        account_page.should_be__page('/account/')

    # @pytest.mark.new_test
    def test_manager_canT_authorization_with_INvalid_email(self, browser, live_server):
        """Тест: возможность залогиниться под НЕвалидными данными """
        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Получаем форму авторизации
        authorization_form_dict = page.should_be_sign_in_form()
        email = "fake@email.com"
        password = "12345"

        # Гость вводит невалидные данные и нажимает кнопку отправить
        page.user_sign_in(email, password, authorization_form_dict)
        # Гость видит сообщение о вводе невалидных данных
        page.should_be_login_error()

    @pytest.mark.django_db
    def test_driver_can_authorization_with_valid_data(self, browser, create_user, live_server):
        """Тест: возможность залогиниться под валидными данными (водитель)"""
        pass

    def test_guest_canT_open_account_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'account'"""

        # Инициализации объекта "Входа"
        page = LoginPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()
        page.go_to__page_by_url(live_server.url + '/account/')
        page.should_be_404_error()

    @pytest.mark.skip
    def guest_canT_open_cars_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'cars'"""
        pass

    @pytest.mark.skip
    def guest_canT_open_drivers_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'drivers'"""
        pass

    @pytest.mark.skip
    def guest_canT_open_cards_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'cards'"""
        pass

    @pytest.mark.skip
    def guest_canT_open_applications_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'applications'"""
        pass

    @pytest.mark.skip
    def guest_canT_open_car_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'car/A111AA/'"""
        pass

    @pytest.mark.skip
    def guest_canT_open_app_page(self, browser, live_server):
        """Тест: гость не может перейти на стр. 'app/1/'"""
        pass
