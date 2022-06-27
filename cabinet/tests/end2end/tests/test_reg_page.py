import time
from unittest import TestCase

import pytest

from cabinet.models import MyUser, CarBrand
from cabinet.tests.end2end.pages.account_page import AccountPage
from cabinet.tests.end2end.pages.base_page import BasePage
from cabinet.tests.end2end.pages.reg_page import RegistrationPage
from django.test import LiveServerTestCase
from cabinet.tests.end2end.pages.login_page import LoginPage

LINK = "/"
class TestRegistrationPage():

    def test_this_is_registration_page(self, browser, live_server):
        """Тест: это стр. регистрации?"""
        # Инициализации объекта "Входа"
        page = RegistrationPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость проверяет, что он на стр. "регистрации"
        page.should_be_registration_page()

    def test_quest_should_see_login_link(self, browser, live_server):
        """Тест: наличие ссылки на стр. авторизации"""

        # Инициализации объекта "Входа"
        page = RegistrationPage(browser, live_server.url + LINK)
        # Гость переходит на стр. авторизации
        page.open()

        # Гость проверяет, что он на стр. "Регистрации"
        page.should_be_login_url()


    def test_quest_can_go_to_registration_page(self, browser, live_server):
        """Тест: возможность перехода на стр. авторизации"""
        pass

    def test_quest_can_go_to_account_activation_page(self, browser):
        """Тест: возможность перехода на стр. регистрации"""
        pass

    def test_guest_should_see_registration_form(self, browser, live_server):
        """Тест: наличие формы регистрации"""

    def test_driver_can_sing_up_with_valid_data(self, browser, create_user, live_server):
        """Тест: возможность зарегистрироваться
        с валидными данными и войти в ЛК """
        pass

    def test_manager_cant_authorization_with_INvalid_email(self, browser, live_server):
        """Тест: возможность зарегистрироваться
         с почтой не записанной в white_list'е
         """
        pass






