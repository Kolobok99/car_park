from selenium.common import NoSuchElementException

from cabinet.models import MyUser
from .base_page import BasePage
from .locators import DriverPageLocators


class DriverPage(BasePage):
    """Стр. выбранного водителя"""

    def should_be_driver_page(self, driver: MyUser):
        """Проверяем, что это нужная стр. авто"""
        self.should_be__page(f"drivers/{driver.pk}")


