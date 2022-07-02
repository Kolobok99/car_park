from selenium.common import NoSuchElementException

from .new_base_page import BasePage
from .new_locators import CarsPageLocators, AccountPageLocators


class CarsPage(BasePage):
    """Стр. всех автомобилей """

    def should_be_cars_page(self):
        """Проверка того, что это стр. 'автомобили"""
        self.should_be__page('/cars/')
