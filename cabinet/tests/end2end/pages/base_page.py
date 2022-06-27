import logging
import math
import sys

import django
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException

from .locators import *
from django.test import LiveServerTestCase


class BasePage():
    """
    Базовая страница, от которой будут унаследованы все остальные классы.
    """


    def __init__(self, browser, url, timeout=5):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, locator, data):
        """Проверяет наличие элемента на стр."""
        try:
            self.browser.find_element(locator, data)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, locator, data, timeout=4):
        """
        Проверяем, что элемент не появился на странице в течении заданного времени.
        """
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((locator, data))
            )
        except TimeoutException:
            return True
        return False

    def user_logout(self):
        """Выход из ЛК"""

        try:
            self.browser.find_element(*HeaderLocators.LOGOUT_BTN).click()
        except NoSuchElementException:
            assert False, "Элемент logout не найден"

    def user_can_go_to_page_by_header(self, page):
        """ фывыфвыф """
        # try:
            # element =  self.browser.find_element()
        pass

