from cabinet.tests.end2end.new_pages.new_base_page import BasePage
from cabinet.tests.end2end.new_pages.new_locators import ActivationPageLocators


class AccountActivationPage(BasePage):

    def should_be_activation_page(self):
        """Проверка того, что это стр. 'login' """
        self.should_be__page('/activation/')

    def should_be_activation_form(self):
        """Проверка наличия формы авторизации"""
        form_dict = {
            'CODE': ActivationPageLocators.FORM_ACTIVATION_INPUT_CODE,
            'BUTTON SUBMIT': ActivationPageLocators.FORM_ACTIVATION_BTN_SUBMIT,
        }
        activation_form_dict = self.should_be_the_(form_dict)
        return activation_form_dict

    def user_activate_account(self, code, form_data):
        """Попытка user'a активировать аккаунт"""

        form_data['CODE'].send_keys(code)
        form_data['BUTTON SUBMIT'].click()