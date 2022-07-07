from selenium.common import NoSuchElementException

from .base_page import BasePage
from .locators import *


class LoginPage(BasePage):
    """Стр. входа в аккаунт user'а"""

    def should_be_login_page(self, live_server):
        """Проверка того, что это стр. 'login' """
        current_url = self.browser.current_url
        assert live_server.url + '/' == current_url, \
            f"This is not {live_server} URL. This is {current_url}"

    def go_to_registration_page_by_href(self):
        """Клик по ссылке <регистрации>"""
        self.go_to__page_by_btn(LoginPageLocators.LINK_BTN_REG, 'регистрация')

    def should_be_sign_in_form(self):
        """Проверка наличия формы авторизации"""
        authorization_form_dict = self.should_be_the_form(LoginPageLocators, 'LOGIN')
        return authorization_form_dict

    def user_sign_in(self, login_data, form_dict):
        """Попытка user'a войти в ЛК"""

        self.form_using(form_dict, login_data)

    def should_be_login_error(self):
        """Проверка наличия вывода ошибки при авторизации"""

        assert self.is_element_present(*LoginPageLocators.FORM_LOGIN_ERROR_LOGIN), \
            "Сообщение об ошибки входа не найдена"

    def guest_canT_go_to_cars_pages(self, live_server):
        """Проверка может ли гость попасть на стр. 'автомобили'"""
        link = '/cars'
        self.browser.get(live_server.url + link)
        self.is_not_element_present(*CarsPageLocators.INFO_CAR_COUNT_TITLE)

