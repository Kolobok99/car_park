from selenium.common import NoSuchElementException

from .new_base_page import BasePage
from .new_locators import *


class LoginPage(BasePage):
    """Стр. входа в аккаунт user'а"""

    def go_to_registration_page_by_href(self):
        """Клик по ссылке <регистрации>"""
        self.go_to__page_by_href_btn(LoginPageLocators.REG_LINK, 'регистрация')

    def should_be_sign_in_form(self):
        form_dict = {
            'EMAIL': LoginPageLocators.EMAIL_INPUT,
            'PASSWORD': LoginPageLocators.PASSWORD_INPUT,
            'BUTTON SUBMIT': LoginPageLocators.BTN_SUBMIT,
        }
        authorization_form_dict = self.should_be_the_form(form_dict)
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