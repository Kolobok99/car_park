from cabinet.tests.end2end.pages.base_page import BasePage
from cabinet.tests.end2end.pages.locators import RegistrationPageLocators


class RegistrationPage(BasePage):

    def should_be_registration_page(self):
        """Проверка того, что это стр. 'registration' """
        self.should_be__page('/registration/')

    def should_be_login_url(self):
        """Проверяет наличие ссылки на стр. 'авторизации'"""
        assert self.is_element_present(*RegistrationPageLocators.LINK_BTN_LOGIN), \
            "Ссылка на стр. <авторизации> не найдена"

    def go_to_login_page_by_href(self):
        """Клик по ссылке <авторизация>"""
        self.go_to__page_by_btn(RegistrationPageLocators.LINK_BTN_LOGIN, 'авторизация')

    def should_be_registration_form(self):
        """Проверка наличия формы авторизации"""
        form_dict = {
            'EMAIL': RegistrationPageLocators.FORM_REG_INPUT_EMAIL,
            'PASSWORD': RegistrationPageLocators.FORM_REG_INPUT_PASS1,
            'PASSWORD2': RegistrationPageLocators.FORM_REG_INPUT_PASS2,
            'FORM_PERSONAL_INPUT_PHONE': RegistrationPageLocators.FORM_REG_INPUT_PHONE,
            'FIRST NAME': RegistrationPageLocators.FORM_REG_INPUT_F_NAME,
            'LAST NAME': RegistrationPageLocators.FORM_REG_INPUT_L_NAME,
            'PATRONYMIC': RegistrationPageLocators.FORM_REG_INPUT_P_NAME,
            'ROLE SELECT': RegistrationPageLocators.FORM_REG_SELECT_ROLE,
            'BUTTON SUBMIT': RegistrationPageLocators.FORM_REG_BTN_SUBMIT,
        }
        registration_form_dict = self.should_be_the_form(form_dict, )
        return registration_form_dict

    def new_should_be_registration_form(self):
        """Проверка наличия формы авторизации"""
        reg_form = self.should_be_the_form(RegistrationPageLocators, "REG")
        return reg_form

    def guest_sign_up_as_driver(self, reg_data, form_dict):
        """Попытка гостя зарегистрироваться как водитель"""

        self.form_using(form_dict, reg_data)
    def should_by_sign_up_errors(self):
        """Проверка наличия сообщений об ошибках"""
        errors_dict = self.should_be_the_form_errors(RegistrationPageLocators, 'REG')
        return errors_dict