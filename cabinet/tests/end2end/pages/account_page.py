from cabinet.tests.end2end.new_pages.new_base_page import BasePage


class AccountPage(BasePage):

    def should_be_account_page(self):
        """Проверка того, что это стр. 'account' """
        self.should_be__page('/account/')

