import pytest

LINK = " "
class TestCarPage:

    @pytest.mark.skip
    def test_this_is_car_page(self, browser, live_server):
        """Тест: это стр. выбраной машины?"""
        pass

    def driver_can_go_to_own_car(self, browser, live_server):
        """Тест: водитель может перейти на стр. своей машины"""
        pass

    def driver_can_go_to_alien_car_page(self, browser, live_server):
        """Тест: водитель может перейти на стр. чужой машины машины"""
        pass

    def test_manager_can_see_form_to_change_cars_data(self, browser, live_server):
        """Тест: менеджер видит форму изменения данных автомобиля"""
        pass

    def test_manager_can_change_car_data_by_valid_data(self, browser, live_server):
        """Тест: менеджер может изменить данные автомобиля (валидными данными)"""
        pass

    def test_manager_canT_change_car_data_by_INvalid_data(self, browser, live_server):
        """Тест: менеджер НЕ может изменить данные автомобиля (НЕвалидными данными)"""
        pass

    def test_manager_can_add_new_app(self, browser, live_server):
        """Тест: менеджер может добавить новую заявку"""
        pass

    def test_manager_can_add_car_doc(self, browser, live_server):
        """Тест: менеджер может добавить новый документ"""
        pass

    def test_manager_canT_add_car_doc_with_invalid_date(self, browser, live_server):
        """Тест: менеджер НЕ может добавить новый документ с невалидной почтой"""
        pass

