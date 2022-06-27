from cabinet.tests.end2end.new_pages.new_base_page import BasePage
from cabinet.tests.end2end.new_pages.new_locators import RegistrationPageLocators


class RegistrationPage(BasePage):

    def should_be_login_url(self):
        """Проверяет наличие ссылки на стр. 'авторизации'"""
        assert self.is_element_present(*RegistrationPageLocators.LOGIN_LINK), \
            "Ссылка на стр. <авторизации> не найдена"

