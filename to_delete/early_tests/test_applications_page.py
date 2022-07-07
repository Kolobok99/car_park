import pytest

from to_delete.early_pages import AccountPage
from to_delete.early_pages import ApplicationsPage
from to_delete.early_pages import LoginPage

LINK = "/applications"
class TestAccountPage:

    def manager_login(self, browser, live_server, create_user):
        """Авторизация менеджера"""
        page = LoginPage(browser, live_server.url)
        page.open()
        login_form = page.should_be_authorization_form()
        test_manager, manager_pass = create_user(role='m')
        page.user_login_with_valid_data(test_manager,manager_pass, login_form)

        account_page = AccountPage(browser, browser.current_url)
        account_page.go_to_applications_page()
        # Инициализация объекта "Регистрация"
        applications_page = ApplicationsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        return applications_page

    @pytest.mark.skip
    def test_this_is_applications_page(self, browser, live_server, create_user):
        """Тест: это стр. 'водители'?"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_drivers_page()

    def test_manager_see_filtration_block(self, browser, live_server, create_user):
        """Тест: менеджер видит блок фильтрации"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_filtration_blocks()


    def test_manager_see_applications_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу заявок"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_drivers_table()

    def test_manager_filter_applications(self, browser, live_server, create_user, create_application):
        """Тест: менеджер проверяет работоспособность фильтра заявок"""
        page = self.manager_login(browser, live_server, create_user)

        new_app1 = create_application()
        new_app2 = create_application()
        new_app3 = create_application()
        new_app4 = create_application()
        new_app5 = create_application()
        new_app6 = create_application()
        new_app7 = create_application()
        new_app8 = create_application()
        new_app9 = create_application()
        new_app10 = create_application()

        filtration_blocks = page.shlould_be_filtration_blocks()
        page.check_filter_results(filtration_blocks)