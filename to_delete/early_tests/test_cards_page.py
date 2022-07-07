import pytest

from to_delete.early_pages import AccountPage
from to_delete.early_pages import CardsPage
from to_delete.early_pages import LoginPage

LINK = "/cards"
class TestCardsPage:
    def manager_login(self, browser, live_server, create_user):
        """Авторизация менеджера"""
        page = LoginPage(browser, live_server.url)
        page.open()
        login_form = page.should_be_authorization_form()
        test_manager, manager_pass = create_user(role='m')
        page.user_login_with_valid_data(test_manager,manager_pass, login_form)

        account_page = AccountPage(browser, browser.current_url)
        account_page.go_to_cards_page()
        # Инициализация объекта "Регистрация"
        cards_page = CardsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        return cards_page



    @pytest.mark.skip
    def test_this_is_cards_page(self, browser, live_server, create_user):
        """Тест: это стр. 'топливные карты'"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cars_page()

    def test_manager_can_add_new_card(self, browser, live_server, create_user):
        """Тест: менеджер может добавить новую топливную карту"""
        page = self.manager_login(browser, live_server, create_user)
        card_add_form = page.should_be_card_add_form()
        page.can_add_card()

    def test_manager_see_filtration_block(self, browser, live_server, create_user):
        """Тест: менеджер видит блок фильтрации"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_filtration_blocks()

    def test_manager_see_cards_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу топливных картов"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cards_table()

    def test_manager_filter_cards(self, browser, live_server, create_user, create_card):
        """Тест: менеджер проверяет работоспособность фильтра топливных карт"""
        page = self.manager_login(browser, live_server, create_user)

        page = self.manager_login(browser, live_server, create_user)

        card_add_form = page.should_be_cards_table()
        new_car1 = page.can_add_card(card_add_form)
        new_car2 = page.can_add_card(card_add_form)
        new_car3 = page.can_add_card(card_add_form)
        new_car4 = page.can_add_card(card_add_form)
        new_car5 = page.can_add_card(card_add_form)
        new_car6 = page.can_add_card(card_add_form)
        new_car7 = page.can_add_card(card_add_form)
        new_car8 = page.can_add_card(card_add_form)
        new_car9 = page.can_add_card(card_add_form)
        new_car10 = page.can_add_card(card_add_form)


        filtration_blocks = page.shlould_be_filtration_blocks()
        page.check_filter_results(filtration_blocks)

    def test_manager_can_delete_cards(self, browser, live_server, create_user):
        """Тест: менеджер может удалить список топливных карт"""
        page = self.manager_login(browser, live_server, create_user)

        card_add_form = page.should_be_card_add_form()
        new_car1 = page.can_add_card(card_add_form)
        new_car2 = page.can_add_card(card_add_form)
        new_car3 = page.can_add_card(card_add_form)
        new_car4 = page.can_add_card(card_add_form)
        new_car5 = page.can_add_card(card_add_form)

        page.can_delete_card(new_car3)

        page.should_be_card(new_car1)
        page.should_be_card(new_car2)
        page.should_be_card(new_car4)
        page.should_be_card(new_car5)


        page.can_delete_card(new_car1, new_car2)

        page.should_be_card(new_car4)
        page.should_be_card(new_car5)

    def test_manager_can_withdraw_cards(self, browser, live_server, create_user):
        """Тест: менеджер может изъять список топливных карт"""

        page = self.manager_login(browser, live_server, create_user)

        card_add_form = page.should_be_card_add_form()
        new_card1 = page.can_add_card(card_add_form)
        new_card2 = page.can_add_card(card_add_form)
        new_card3 = page.can_add_card(card_add_form)
        new_card4 = page.can_add_card(card_add_form)
        new_card5 = page.can_add_card(card_add_form)

        page.can_withdraw_card(new_card3)

        page.should_be_card(new_card1)
        page.should_be_card(new_card2)
        page.should_be_card(new_card4)
        page.should_be_card(new_card5)

        page.can_withdraw_card(new_card1, new_card2)

        page.should_be_card(new_card4)
        page.should_be_card(new_card5)