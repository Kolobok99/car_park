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

    # @classmethod
    # def setUpClass(cls):
    #     super(cls).setUpClass()
    #     django.setup()
    #     logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    def __init__(self, browser, url, timeout=5):
        super().__init__()
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)
        # self.browser.get(('%s%s' % (self.live_server_url, '/admin/')))

    def is_element_present(self, locator, data):
        """Проверяет наличие элемента на стр."""
        try:
            self.browser.find_element(locator, data)
        except NoSuchElementException:
            return False
        return True