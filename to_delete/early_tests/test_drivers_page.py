from to_delete.early_pages import AccountPage
from to_delete.early_pages import DriversPage
from to_delete.early_pages import LoginPage

LINK = "/drivers"
class TestDriversPage:
    def manager_login(self, browser, live_server, create_user):
        """Авторизация менеджера"""
        page = LoginPage(browser, live_server.url)
        page.open()
        login_form = page.should_be_authorization_form()
        test_manager, manager_pass = create_user(role='m')
        page.user_login_with_valid_data(test_manager,manager_pass, login_form)

        account_page = AccountPage(browser, browser.current_url)
        account_page.go_to_drivers_page()
        # Инициализация объекта "Регистрация"
        drivers_page = DriversPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        return drivers_page


    # @pytest.mark.skip
    def test_this_is_drivers_page(self, browser, live_server, create_user):
        """Тест: это стр. 'водители'?"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_drivers_page()

    def test_manager_see_filtration_block(self, browser, live_server, create_user):
        """Тест: менеджер видит блок фильтрации"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_filtration_blocks()

    def test_manager_see_drivers_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу водителей"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cars_table()

    def test_manager_filter_drivers(self, browser, live_server, create_user, create_driver):
        """Тест: менеджер проверяет работоспособность фильтра водителей"""
        page = self.manager_login(browser, live_server, create_user)

        new_driver1 = create_driver()
        new_driver2 = create_driver()
        new_driver3 = create_driver()
        new_driver4 = create_driver()
        new_driver5 = create_driver()
        new_driver6 = create_driver()
        new_driver7 = create_driver()
        new_driver8 = create_driver()
        new_driver9 = create_driver()
        new_driver10 = create_driver()

        filtration_blocks = page.shlould_be_filtration_blocks()
        page.check_filter_results(filtration_blocks)