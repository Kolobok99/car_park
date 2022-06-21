from cabinet.tests.end2end.pages.base_page import BasePage


class AccountPage(BasePage):

    def should_be_account_page(self):
        url = "/account/"
        current_url = self.browser.current_url
        assert self.browser.current_url.endswith(f"{url}"), \
            f"This is not {url} URL. This is {current_url}"