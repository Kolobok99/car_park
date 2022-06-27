import pytest

from cabinet.models import MyUser, CarBrand
from cabinet.tests.end2end.pages.account_page import AccountPage
from cabinet.tests.end2end.pages.reg_page import RegistrationPage
from cabinet.tests.end2end.pages.login_page import LoginPage

LINK = ""
class TestAppPage:

    @pytest.mark.skip
    def test_this_is_app_page(self, browser, live_server):
        """Тест: это стр. выбранной 'заявки'"""
        pass

    # --------- МЕНЕДЕЖЕР --------- #

    def test_manager_see_information_about_app(self, browser, live_server):
        """Тест: менеджер видит всю информацию о выбранной заявке"""
        pass

    def test_manager_see_change_btn_on_the_own_app_page(self, browser, live_server):
        """Тест: менеджер видит кнопку редактирования у своей записи"""
        pass

    def test_manager_see_delete_btn_on_the_own_app_page(self, browser, live_server):
        """Тест: менеджер видит кнопку удаления у своей записи"""
        pass

    def test_manager_not_see_access_btn_on_the_own_app_page(self, browser, live_server):
        """Тест: менеджер НЕ видит кнопку подтверждения у своей записи"""
        pass

    def test_manager_not_see_return_btn_on_the_own_app_page(self, browser, live_server):
        """Тест: менеджер НЕ видит кнопку возвращения на доработку у своей записи"""
        pass

    def test_manager_can_change_own_app(self, browser, live_server):
        """Тест: менеджер может изменить собственную заявку"""
        pass

    def test_manager_can_delete_own_app(self, browser, live_server):
        """Тест: менеджер может удалить собственную заявку"""
        pass

    # --------- ВОДИТЕЛЬ --------- #

    def test_driver_see_information_about_own_app(self, browser, live_server):
        """Тест: водитель видит всю информацию о своей заявке"""
        pass

    def test_driver_see_change_btn_on_the_own_app_page(self, browser, live_server):
        """Тест: водитель видит кнопку редактирования у своей записи"""
        pass

    def test_driver_see_delete_btn_on_the_own_app_page(self, browser, live_server):
        """Тест: водитель видит кнопку удаления у своей записи"""
        pass

    def test_driver_can_change_own_app(self, browser, live_server):
        """Тест: водитель может изменить собственную заявку"""
        pass

    def test_driver_can_delete_own_app(self, browser, live_server):
        """Тест: водитель может удалить собственную заявку"""
        pass


