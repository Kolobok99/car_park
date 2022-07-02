from cabinet.tests.end2end.new_pages.new_base_page import BasePage
from cabinet.tests.end2end.new_pages.new_locators import RegistrationPageLocators


class RegistrationPage(BasePage):

    def should_be_registration_page(self):
        """Проверка того, что это стр. 'registration' """
        self.should_be__page('/registration/')

    def should_be_login_url(self):
        """Проверяет наличие ссылки на стр. 'авторизации'"""
        assert self.is_element_present(*RegistrationPageLocators.LOGIN_LINK_BTN), \
            "Ссылка на стр. <авторизации> не найдена"

    def go_to_login_page_by_href(self):
        """Клик по ссылке <авторизация>"""
        self.go_to__page_by_btn(RegistrationPageLocators.LOGIN_LINK_BTN, 'авторизация')

    def should_be_registration_form(self):
        """Проверка наличия формы авторизации"""
        form_dict = {
            'EMAIL': RegistrationPageLocators.EMAIL_INPUT,
            'PASSWORD': RegistrationPageLocators.FORM_REG_INPUT_PASS1,
            'PASSWORD2': RegistrationPageLocators.FORM_REG_INPUT_PASS2,
            'FORM_PERSONAL_INPUT_PHONE': RegistrationPageLocators.FORM_REG_INPUT_PHONE,
            'FIRST NAME': RegistrationPageLocators.FORM_REG_INPUT_F_NAME,
            'LAST NAME': RegistrationPageLocators.FORM_REG_INPUT_L_NAME,
            'PATRONYMIC': RegistrationPageLocators.FORM_REG_INPUT_P_NAME,
            'ROLE SELECT': RegistrationPageLocators.ROLE_SELECT,
            'BUTTON SUBMIT': RegistrationPageLocators.SUBMIT_BTN,
        }
        registration_form_dict = self.should_be_the_(form_dict)
        return registration_form_dict

    def guest_sign_up_as_driver(self, reg_data, form_data):
        """Попытка гостя зарегистрироваться как водитель"""


        form_data['EMAIL'].send_keys(reg_data['email'])
        form_data['PASSWORD'].send_keys(reg_data['pass1'])
        form_data['PASSWORD2'].send_keys(reg_data['pass2'])
        form_data['FORM_PERSONAL_INPUT_PHONE'].send_keys(reg_data['phone'])
        form_data['FIRST NAME'].send_keys(reg_data['f_name'])
        form_data['LAST NAME'].send_keys(reg_data['l_name'])
        form_data['PATRONYMIC'].send_keys(reg_data['p_name'])
        form_data['BUTTON SUBMIT'].click()

    def should_by_sign_up_errors(self):
        """Проверка наличия сообщений об ошибках"""
        errors_dict = {
            'FORM_REG_ERROR_EMAIL': RegistrationPageLocators.FORM_REG_ERROR_EMAIL,
            'PASSWORD_ERROR': RegistrationPageLocators.PASS_ERROR,
            'FORM_REG_ERROR_PHONE': RegistrationPageLocators.FORM_REG_ERROR_PHONE,
            'FORM_REG_ERROR_F_NAME': RegistrationPageLocators.FORM_REG_ERROR_F_NAME,
            'FORM_REG_ERROR_L_NAME': RegistrationPageLocators.FORM_REG_ERROR_L_NAME,
            'FORM_REG_ERROR_P_NAME': RegistrationPageLocators.FORM_REG_ERROR_P_NAME,
        }
        self.should_be_the_(errors_dict)