from selenium.common import NoSuchElementException

from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    """Стр. входа в аккаунт user'а"""


    def should_be_login_page(self):
        """ asd"""
        text = ""
        assert self.browser.current_url.endswith(f"{text}"), \
            f"This is not {text} URL."

    def should_be_registration_url(self):
        assert self.is_element_present(*LoginPageLocators.REG_LINK), \
            "Ссылка на стр. <регистрации> не найдена"

    def should_be_account_activation_link(self):
        assert self.is_element_present(*LoginPageLocators.REG_LINK), \
            "Ссылка на стр. <активации аккаунта> не найдена"

    def should_be_account_password_change_link(self):
        assert self.is_element_present(*LoginPageLocators.PASSWORD_CHANGE_LINK), \
            "Ссылка на стр. <смены пароля> не найдена"

    def go_to_registration_page(self):
        """Клик по ссылке <регистрации>"""
        try:
            login_link = self.browser.find_element(*LoginPageLocators.REG_LINK)
        except NoSuchElementException:
            assert False, "Ссылка на стр. <регистрации> на найдена"
        else:
            login_link.click()

    def should_be_authorization_form(self):
        """Проверка наличия формы авторизации"""
        elements_exception = []
        try:
            email_input = self.browser.find_element(*LoginPageLocators.EMAIL_INPUT)
        except NoSuchElementException:
            elements_exception.append("EMAIL")

        try:
            pass_input = self.browser.find_element(*LoginPageLocators.PASSWORD_INPUT)
        except NoSuchElementException:
            elements_exception.append("PASSWORD")

        try:
            btn_submit = self.browser.find_element(*LoginPageLocators.BTN_SUBMIT)
        except NoSuchElementException:
            elements_exception.append("BUTTON SUBMIT")

        if elements_exception:
            assert False, f"Не найдены следующие эл. формы: {elements_exception}"
        else:
            return {
                'email_input': email_input,
                'pass_input': pass_input,
                'btn_submit': btn_submit
            }

    def manager_can_login_with_valid_data(self, test_manager, password, form_data):
        """Попытка войти юсера с валидными данными"""

        print(f"{test_manager.email=}")
        form_data['email_input'].send_keys(test_manager.email)
        form_data['pass_input'].send_keys(password)
        form_data['btn_submit'].click()








