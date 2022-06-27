from cabinet.tests.end2end.pages.base_page import BasePage
from cabinet.tests.end2end.pages.locators import RegistrationPageLocators


class RegistrationPage(BasePage):

    def should_be_registration_page(self):
        url = "/registration/"
        current_url = self.browser.current_url
        assert self.browser.current_url.endswith(f"{url}"), \
            f"This is not {url} URL. This is {current_url}"

    def should_be_login_url(self):
        """Проверяет наличие ссылки на стр. 'авторизации'"""
        assert self.is_element_present(*RegistrationPageLocators.LOGIN_LINK), \
            "Ссылка на стр. <авторизации> не найдена"

