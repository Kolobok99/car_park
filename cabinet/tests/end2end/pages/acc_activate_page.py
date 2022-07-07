from cabinet.tests.end2end.pages.base_page import BasePage
from cabinet.tests.end2end.pages.locators import ActivationPageLocators


class AccountActivationPage(BasePage):

    def should_be_activation_page(self):
        """Проверка того, что это стр. 'login' """
        self.should_be__page('/activation/')

    def should_be_activation_form(self):
        """Проверка наличия формы авторизации"""
        activation_form_dict = self.should_be_the_form(ActivationPageLocators, "ACTIVATION")
        return activation_form_dict

    def user_activate_account(self, activate_data, form_dict):
        """Попытка user'a активировать аккаунт"""

        self.form_using(form_dict, activate_data)