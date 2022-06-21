from cabinet.tests.end2end.pages.base_page import BasePage


class RegistrationPage(BasePage):

    def should_be_registration_page(self):
        url = "/registration/"
        current_url = self.browser.current_url
        assert self.browser.current_url.endswith(f"{url}"), \
            f"This is not {url} URL. This is {current_url}"