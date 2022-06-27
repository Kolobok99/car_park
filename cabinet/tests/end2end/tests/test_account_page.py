import pytest

from cabinet.models import MyUser, CarBrand
from cabinet.tests.end2end.pages.account_page import AccountPage
from cabinet.tests.end2end.pages.cars_page import CarsPage
from cabinet.tests.end2end.pages.reg_page import RegistrationPage
from cabinet.tests.end2end.pages.login_page import LoginPage




LINK = "/account/"
class TestAccountPage:


    def manager_login(self, browser, live_server, create_user):
        """Авторизация менеджера"""
        page = LoginPage(browser, live_server.url)
        page.open()
        login_form = page.should_be_authorization_form()
        test_manager, manager_pass = create_user(role='m')
        page.user_login_with_valid_data(test_manager,manager_pass, login_form)

        account_page = AccountPage(browser, browser.current_url)

        return account_page

    def test_this_is_account_page(self, browser, live_server, create_user):
        """Тест: это стр. ЛК?"""

        page = self.manager_login(browser, live_server, create_user)
        page.should_be_account_page()


     # -------- МЕНЕДЖЕР ----- #

    def test_manager_can_logount(self, browser, live_server, create_user):
        """Тест: менеджер может выйти из ЛК"""
        page = self.manager_login(browser, live_server, create_user)
        page.user_logout()
        login_page = LoginPage(browser, browser.current_url)
        login_page.guest_canT_go_to_cars_pages(live_server)


    def test_manager_can_go_to_cars_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'cars'"""
        page = self.manager_login(browser, live_server, create_user)
        # Гость нажимает на кнопку "Регистрации
        page.go_to_cars_page()
        # Инициализация объекта "Регистрация"
        cars_page = CarsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        cars_page.should_be_cars_page()

    def test_manager_can_go_to_drivers_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'drivers'"""
        page = self.manager_login(browser, live_server, create_user)
        # Гость нажимает на кнопку "Регистрации
        page.go_to_drivers_page()
        # Инициализация объекта "Регистрация"
        cars_page = CarsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        cars_page.should_be_drivers_page()

    def test_manager_can_go_to_documents_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'documents'"""
        page = self.manager_login(browser, live_server, create_user)
        # Гость нажимает на кнопку "Регистрации
        page.go_to_documents_page()
        # Инициализация объекта "Регистрация"
        cars_page = CarsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        cars_page.should_be_documents_page()

    def test_manager_can_go_to_cards_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'cards'"""
        page = self.manager_login(browser, live_server, create_user)
        # Гость нажимает на кнопку "Регистрации
        page.go_to_cards_page()
        # Инициализация объекта "Регистрация"
        cars_page = CarsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        cars_page.should_be_cards_page()

    def test_manager_can_go_to_applications_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. 'applications'"""
        page = self.manager_login(browser, live_server, create_user)
        page.manager_can_go_to_applications_page()

    def test_manager_see_form_to_change_personal_data(self, browser, live_server, create_user):
        """Тест: менеджер видит форму изменения личных данных"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_form_to_change_data()

    def test_manager_can_change_personal_data_by_valid_data(self, browser, live_server, create_user):
        """Тест: менеджер может изменить личные данные (валидными данными)"""
        page = self.manager_login(browser, live_server, create_user)
        change_form = page.should_be_form_to_change_data()
        page.can_change_data_by_valid_data()



    def test_manager_canT_change_personal_data_by_INvalid_data(self, browser, live_server, create_user):
        """Тест: менеджер НЕ может изменить личные данные (НЕвалидными данными)"""
        page = self.manager_login(browser, live_server, create_user)
        change_form = page.should_be_form_to_change_data()
        page.canT_change_data_by_INvalid_data()

    def test_manager_see_cars_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу 'машины' """
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cars_table()
    def test_manager_see_applications_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу 'заявки' """
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_applications_table()

    def test_manager_see_cards_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу 'топливные картиы' """
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cards_table()
    def test_manager_see_docs_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу 'документы' """
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cards_table()

    def test_manager_can_add_doc(self, browser, live_server, create_user):
        """Тест: менеджер может добавить документ """
        page = self.manager_login(browser, live_server, create_user)
        form_add_doc = page.should_be_form_to_add_doc()
        page.can_add_doc()

    def test_manager_canT_add_doc_with_invalid_date(self, browser, live_server, create_user):
        """Тест: водитель НЕ может добавить новый документ с невалидной почтой"""
        page = self.manager_login(browser, live_server, create_user)
        form_add_doc = page.should_be_form_to_add_doc()
        page.canT_add_doc_with_invalid_data()






     # -------- ВОДИТЕЛЬ ----- #

    def driver_can_logount(self, browser, live_server):
        """Тест: водитель может выйти из ЛК"""
        pass
    def test_driver_canT_go_to_cars_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'cars'"""
        pass

    def test_driver_canT_go_to_drivers_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'drivers'"""
        pass

    def test_driver_canT_go_to_documents_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'documents'"""
        pass

    def test_driver_canT_go_to_cards_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'cards'"""
        pass

    def test_driver_canT_go_to_applications_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. 'applications'"""
        pass

    def test_driver_can_see_form_to_change_personal_data(self, browser, live_server):
        """Тест: менеджер видит форму изменения личных данных"""
        pass

    def test_driver_can_change_personal_data_by_valid_data(self, browser, live_server):
        """Тест: водитель может изменить личные данные (валидными данными)"""
        pass

    def test_driver_see_cars_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'машины' """
        pass
    def test_driver_see_applications_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'заявки' """
        pass
    def test_driver_see_cards_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'топливные карты' """
        pass
    def test_driver_see_docs_table(self, browser, live_server):
        """Тест: водитель видит таблицу 'документы' """
        pass

    def test_driver_can_add_doc(self, browser, live_server):
        """Тест: водитель может добавить документ """
        pass

    def test_driver_canT_add_doc_with_invalid_date(self, browser, live_server):
        """Тест: водитель НЕ может добавить новый документ с невалидной почтой"""
        pass
