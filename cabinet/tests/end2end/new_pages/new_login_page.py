from selenium.common import NoSuchElementException

from .new_base_page import BasePage
from .new_locators import *


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
        form_dict = {
            'EMAIL': LoginPageLocators.FORM_LOGIN_INPUT_EMAIL,
            'PASSWORD': LoginPageLocators.FORM_LOGIN_INPUT_PASSWORD,
            'BUTTON SUBMIT': LoginPageLocators.BTN_SUBMIT,
        }
        authorization_form_dict = self.should_be_the_(form_dict)
        return authorization_form_dict

    def user_sign_in(self, email, password, form_data):
        """Попытка user'a войти в ЛК"""

        form_data['EMAIL'].send_keys(email)
        form_data['PASSWORD'].send_keys(password)
        form_data['BUTTON SUBMIT'].click()

    def should_be_login_error(self):
        """Проверка наличия вывода ошибки при авторизации"""

        assert self.is_element_present(*LoginPageLocators.LOGIN_ERROR), \
            "Сообщение об ошибки входа не найдена"

    def guest_canT_go_to_cars_pages(self, live_server):
        """Проверка может ли гость попасть на стр. 'автомобили'"""
        link = '/cars'
        self.browser.get(live_server.url + link)
        self.is_not_element_present(*CarsPageLocators.CAR_TITLE_COUNT)
