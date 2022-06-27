from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException

from .new_locators import *

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

    def should_be__page(self, url):
        """Проверка ю ю ю """
        current_url = self.browser.current_url
        assert self.browser.current_url.endswith(f"{url}"), \
            f"This is not {url} URL. This is {current_url}"

    def go_to__page_by_href_btn(self, locator, page_name):
        """Клик по кнопке перехода на другую страницу"""
        """Клик по ссылке < . . .>"""
        try:
            link = self.browser.find_element(*locator)
        except NoSuchElementException:
            assert False, f"Ссылка на стр. <{page_name}> не найдена"
        else:
            link.click()

    def go_to__page_by_url(self, url):
        """Переход на стр. < . . . >"""
        self.browser.get(url)

    def should_be_the_form(self, form_dict):
        """Проверка наличия формы < . . .>"""
        elements_exception = []
        return_dict = {}
        for form_key in form_dict:
            try:
                form_input = self.browser.find_element(*form_dict[form_key])
                return_dict[form_key] = form_input
            except NoSuchElementException:
                elements_exception.append(form_key)

        if elements_exception:
            assert False, f"Не найдены следующие эл. формы: {elements_exception}"
        else:
            return return_dict

    def should_be_404_error(self):
        """Проверка наличия ошибки 404 на стр."""
        self.is_element_present(*HeaderLocators.ERROR_404)