from selenium.common import NoSuchElementException

from .base_page import BasePage
from .locators import CarsPageLocators


class CarsPage(BasePage):
    """Стр. всех автомобилей """

    def should_be_cars_page(self):
        """Проверка того, что это стр. 'автомобили"""
        pass

    def should_be_car_add_form(self):
        """Проверка наличия формы добавления автомобиля"""
        pass

    def can_add_car(self, car_add_form):
        """Проверка возможности добавления автомобиля"""
        pass
    def go_to_car_page(self, car_number):
        """Проверка перхода на стр. выбранного автомобиля"""
        pass

    def shlould_be_filtration_blocks(self):
        """Проверка наличия блоков фильтрации"""
        pass

    def should_be_cars_table(self):
        """Провекра наличия таблицы автомобилей"""
        pass

    def check_filter_results(self):
        """Формирует условия фильтрации и проверяет достоверность результата"""
        pass

    def can_delete_car(self, *args):
        """Проеряет возможность удаления списка автомобилей"""
        pass

    def should_be_car(self, car):
        """Проверяет наличия автомобиля в таблице"""
        pass

    def can_withdraw_car(self, *args):
        """Проеряет возможность изъятия списка автомобилей"""
        pass



