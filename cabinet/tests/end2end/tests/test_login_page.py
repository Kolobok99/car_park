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
class TestLoginPage():

    # @pytest.mark.skip
    # def test_this_is_login_page(self, browser):
    #     """Тест: это стр. авторизации?"""
    #     page = LoginPage(browser, LINK)
    #     page.open()
    #     page.should_be_login_page()
    #
    # @pytest.mark.skip
    # def test_quest_should_see_registration_link(self, browser):
    #     """Тест: наличие ссылки на стр. регистрации"""
    #     # assert 1 is 1
    #     page = LoginPage(browser, LINK)
    #     page.open()
    #     page.should_be_registration_url()
    #
    # @pytest.mark.skip
    # def test_quest_can_go_to_registration_page(self, browser):
    #     """Тест: возможность перехода на стр. регистрации"""
    #     page = LoginPage(browser, LINK)
    #     page.open()
    #     page.go_to_registration_page()
    #
    #     reg_page = RegistrationPage(browser, browser.current_url)
    #     reg_page.should_be_registration_page()
    #
    # @pytest.mark.skip
    # def test_quest_should_see_account_activation_link(self, browser):
    #     """Тест: наличие ссылки на стр. активации аккаунта"""
    #     # assert 1 is 1
    #     page = LoginPage(browser, LINK)
    #     page.open()
    #     page.should_be_account_activation_link()
    #
    # @pytest.mark.skip
    # def test_quest_can_go_to_account_activation_page(self, browser):
    #     """Тест: возможность перехода на стр. регистрации"""
    #     pass
    #
    # # @pytest.mark.xfail
    # @pytest.mark.skip
    # def test_quest_should_see_password_change_link(self, browser):
    #     """Тест: наличие ссылки на стр. смены пароля"""
    #     # assert 1 is 1
    #     page = LoginPage(browser, LINK)
    #     page.open()
    #     page.should_be_account_password_change_link()
    #
    # @pytest.mark.skip
    # def test_guest_should_see_authorization_form(self, browser):
    #     """Тест: наличие формы авторизации"""
    #     page = LoginPage(browser, LINK)
    #     page.open()
    #     page.should_be_authorization_form()
    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_manager_can_authorization_with_valid_data(self, browser, create_manager, live_server):
        page = LoginPage(browser, live_server.url + LINK)

        page.open()

        authorization_form_dict = page.should_be_authorization_form()
        test_manager, password = create_manager

        page.manager_can_login_with_valid_data(test_manager, password, authorization_form_dict)

        account_page = AccountPage(browser, browser.current_url)
        account_page.should_be_account_page()

