import pytest

from cabinet.models import MyUser, CarBrand
from cabinet.tests.end2end.pages.account_page import AccountPage
from cabinet.tests.end2end.pages.cars_page import CarsPage
from cabinet.tests.end2end.pages.reg_page import RegistrationPage
from cabinet.tests.end2end.pages.login_page import LoginPage

LINK = "/cars"
class TestCarsPage:

    def manager_login(self, browser, live_server, create_user):
        """Авторизация менеджера"""
        page = LoginPage(browser, live_server.url)
        page.open()
        login_form = page.should_be_authorization_form()
        test_manager, manager_pass = create_user(role='m')
        page.user_login_with_valid_data(test_manager,manager_pass, login_form)

        account_page = AccountPage(browser, browser.current_url)
        account_page.go_to_cars_page()
        # Инициализация объекта "Регистрация"
        cars_page = CarsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        return cars_page


    # @pytest.mark.skip
    def test_this_is_cars_page(self, browser, live_server, create_user):
        """Тест: это стр. 'автомобили'?"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cars_page()

    def test_manager_can_add_new_car(self, browser, live_server, create_user):
        """Тест: менеджер может добавить новую машину"""
        page = self.manager_login(browser, live_server, create_user)
        car_add_form = page.should_be_car_add_form()
        page.can_add_car(car_add_form)

    def test_manager_can_go_to_car_page(self, browser, live_server, create_user):
        """Тест: менеджер может перейти на стр. выбранной машины"""
        page = self.manager_login(browser, live_server, create_user)
        car_add_form = page.should_be_car_add_form()
        new_car = page.can_add_car(car_add_form)
        page.go_to_car_page(new_car)

    def test_manager_see_filtration_blocks(self, browser, live_server, create_user):
        """Тест: менеджер видит блок фильтрации"""
        page = self.manager_login(browser, live_server, create_user)
        page.shlould_be_filtration_blocks()



    def test_manager_see_cars_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу машин"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cars_table()
    def test_manager_filter_cars(self, browser, live_server, create_user):
        """Тест: менеджер проверяет работоспособность фильтра машин"""
        page = self.manager_login(browser, live_server, create_user)

        car_add_form = page.should_be_car_add_form()
        new_car1 = page.can_add_car(car_add_form)
        new_car2 = page.can_add_car(car_add_form)
        new_car3 = page.can_add_car(car_add_form)
        new_car4 = page.can_add_car(car_add_form)
        new_car5 = page.can_add_car(car_add_form)
        new_car6 = page.can_add_car(car_add_form)
        new_car7 = page.can_add_car(car_add_form)
        new_car8 = page.can_add_car(car_add_form)
        new_car9 = page.can_add_car(car_add_form)
        new_car10 = page.can_add_car(car_add_form)

        filtration_blocks = page.shlould_be_filtration_blocks()
        page.check_filter_results(filtration_blocks)


    def test_manager_can_delete_cars(self, browser, live_server, create_user):
        """Тест: менеджер может удалить список машиин"""
        page = self.manager_login(browser, live_server, create_user)

        car_add_form = page.should_be_car_add_form()
        new_car1 = page.can_add_car(car_add_form)
        new_car2 = page.can_add_car(car_add_form)
        new_car3 = page.can_add_car(car_add_form)
        new_car4 = page.can_add_car(car_add_form)
        new_car5 = page.can_add_car(car_add_form)

        page.can_delete_car(new_car3)

        page.should_be_car(new_car1)
        page.should_be_car(new_car2)
        page.should_be_car(new_car4)
        page.should_be_car(new_car5)


        page.can_delete_car(new_car1, new_car2)

        page.should_be_car(new_car4)
        page.should_be_car(new_car5)



    def test_manager_can_withdraw_cars(self, browser, live_server, create_user):
        """Тест: менеджер может изъять список машиин"""

        page = self.manager_login(browser, live_server, create_user)

        car_add_form = page.should_be_car_add_form()
        new_car1 = page.can_add_car(car_add_form)
        new_car2 = page.can_add_car(car_add_form)
        new_car3 = page.can_add_car(car_add_form)
        new_car4 = page.can_add_car(car_add_form)
        new_car5 = page.can_add_car(car_add_form)

        page.can_withdraw_car(new_car3)

        page.should_be_car(new_car1)
        page.should_be_car(new_car2)
        page.should_be_car(new_car4)
        page.should_be_car(new_car5)

        page.can_withdraw_car(new_car1, new_car2)

        page.should_be_car(new_car4)
        page.should_be_car(new_car5)


