from selenium.common import NoSuchElementException

from .base_page import BasePage
from .locators import CarPageLocators


class CarPage(BasePage):
    """Стр. выбранного автомобиля """

    def should_be_car_page(self, reg_number):
        """Проверяем, что это нужная стр. авто"""
        self.should_be__page(reg_number)

