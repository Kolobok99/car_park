import re
import time

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException, \
    StaleElementReferenceException

from .locators import *

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

    def reload(self):
        """Перезагрузка стр."""
        self.browser.refresh()

    def logout(self):
        """Выход из ЛК"""
        try:
            self.browser.find_element(*HeaderLocators.LINK_BTN_LOGOUT).click()
        except NoSuchElementException:
            assert False, "Элемент logout не найден"

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

    def go_to__page_by_btn(self, locator, page_name):
        """Клик по кнопке перехода на другую страницу
        Клик по ссылке < . . .>
        """
        try:
            link = self.browser.find_element(*locator)
        except NoSuchElementException:
            assert False, f"Ссылка на стр. <{page_name}> не найдена"
        else:
            link.click()

    def go_to_cars_page_by_btn(self):
        """Переход на стр. "Машины" через header"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_CARS, "Машины")

    def go_to_cars_drivers_by_btn(self):
        """Переход на стр. "Водители" через header"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_DRIVERS, "Водители")

    def go_to_drivers_page_by_btn(self):
        """Переход на стр. "Топливные карты" через header"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_DRIVERS, "Топливные карты")

    def go_to_docs_page_by_btn(self):
        """Переход на стр. "Документы" через header"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_DOCS, "Документы")

    def go_to_apps_page_by_btn(self):
        """Переход на стр. "Заявки карты" через header"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_APPS, "Заявки")

    def go_to__page_by_url(self, url):
        """Переход на стр. < . . . >"""
        self.browser.get(url)

    def should_be_the_form(self, page_locators, form_name):
        """Проверка наличия элементов < формы, таблицы >"""
        form_dict = self.form_dict_generator(page_locators, form_name)
        elements_exception = []
        return_dict = {}
        for form_key in form_dict:
            try:
                form_input = self.browser.find_element(*form_dict[form_key])
                return_dict[form_key] = form_input
            except NoSuchElementException:
                elements_exception.append(form_key)


        if elements_exception:
            assert False, f"Не найдены следующие элементы: {elements_exception}"
        else:
            return return_dict

    def should_be_the_form_errors(self, page_locators, form_name):
        """Проверка наличия элементов < формы, таблицы >"""
        form_dict = self.errors_dict_generator(page_locators, form_name)
        elements_exception = []
        return_dict = {}
        for form_key in form_dict:
            try:
                form_input = self.browser.find_element(*form_dict[form_key])
                return_dict[form_key] = form_input
            except NoSuchElementException:
                elements_exception.append(form_key)

        if elements_exception:
            assert False, f"Не найдены следующие элементы: {elements_exception}"
        else:
            return return_dict

    def should_be_the_table(self, page_locators, table_name):
        """Проверка наличия элементов таблицы < . . . >"""
        form_dict = self.table_dict_generator(page_locators, table_name)
        elements_exception = []
        return_dict = {}
        for form_key in form_dict:
            try:
                form_input = self.browser.find_element(*form_dict[form_key])
                return_dict[form_key] = form_input
            except NoSuchElementException:
                elements_exception.append(form_key)

        if elements_exception:
            assert False, f"Не найдены следующие элементы: {elements_exception}"
        else:
            return return_dict

    def should_be_the_filter_blocks(self, page_locators, table_name):
        """Проверка наличия элементов таблицы < . . . >"""
        filters_dict = self.filters_dict_generator(page_locators, table_name)
        elements_exception = []
        return_dict = {}
        for filter_key in filters_dict:
            try:
                if 'CHECKS' in filter_key:
                    form_input = self.browser.find_elements(*filters_dict[filter_key])
                else:
                    form_input = self.browser.find_element(*filters_dict[filter_key])
                return_dict[filter_key] = form_input
            except NoSuchElementException:
                elements_exception.append(filter_key)

        if elements_exception:
            assert False, f"Не найдены следующие элементы: {elements_exception}"
        else:
            # print(return_dict['FILTER_CARS_REG_NUMBER_INPUT'])
            return return_dict

    def should_be_NOT_the_table(self, locator):
        """Проверка, того, что на стр. нет таблицы"""
        if self.is_element_present(*locator):
            return True
        else:
            return False
    def should_be_404_error(self):
        """Проверка наличия ошибки 404 на стр."""
        self.is_element_present(*HeaderLocators.PAGE_ERROR_404)

    def go_to_cars_page_by_btn(self):
        """Переход на стр. '' посредством нажатия кнопки"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_CARS, 'машины')

    def go_to_drivers_page_by_btn(self):
        """Переход на стр. '' посредством нажатия кнопки"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_DRIVERS, 'водители')

    def go_to_docs_page_by_btn(self):
        """Переход на стр. '' посредством нажатия кнопки"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_DOCS, 'документы')

    def go_to_cards_page_by_btn(self):
        """Переход на стр. '' посредством нажатия кнопки"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_CARDS, 'топливные карты')

    def go_to_apps_page_by_btn(self):
        """Переход на стр. '' посредством нажатия кнопки"""
        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_APPS, 'заявки')

    def go_to__page_by_table_row(self, table_name, row_text):
        """Переход на запись <машины или заявки>
        по табличной ссылке
        """
        try:
            url_btn = self.browser.find_element(
                By.XPATH, f"//*[contains(@class,'{table_name}')]//td[contains(@class,'table__cell')]//a[contains(text(), '{row_text}')]")
        except NoSuchElementException:
            assert False, f"Кнопка для перехода на запись {row_text} не найдена"

        url_btn.click()

    def is_row_in_table(self, table_name, row_text):
        """Проверяет наличие записи в таблице"""
        try:
            self.browser.find_element(By.XPATH, f"//*[contains(@class,'{table_name}')]//td[contains(@class,'table__cell')][text() = '{row_text}']")
        except NoSuchElementException:
            return False
        return True

    def close_message(self, msg_locator, cross_locator):
        """Закрывает сообщение"""

        try:
            self.is_element_present(*msg_locator)
        except NoSuchElementException:
            assert False, "Сообщение не найдено!"

        try:
            msg_cross = self.browser.find_element(*cross_locator)
            msg_cross.click()
        except NoSuchElementException:
            assert False, "Крестик не найден"

        try:
            self.is_not_element_present(*msg_locator)
        except NoSuchElementException:
            assert False, "Сообщение не исчезло после закрытия"


    def form_dict_generator(self, page_locators, form_name):
        """Генерирует словарь данных формы"""
        form_attr_list = [i for i in dir(page_locators) if re.fullmatch(fr"FORM_{form_name}_(INPUT|BTN|RADIO|CHECKS|SELECT).*", i)]
        new_dict = {}
        for elem in form_attr_list:
            new_dict[elem] = getattr(page_locators, elem)

        return new_dict

    def errors_dict_generator(self, page_locators, form_name):
        """Генерирует словарь ошибок формы"""
        form_errors_list = [i for i in dir(page_locators) if
                          re.fullmatch(fr"FORM_{form_name}_ERROR.*", i)]
        new_dict = {}
        for elem in form_errors_list:
            new_dict[elem] = getattr(page_locators, elem)

        return new_dict

    def table_dict_generator(self, page_locators, table_name):
        """Генерирует словарь ошибок формы"""
        form_errors_list = [i for i in dir(page_locators) if
                            re.fullmatch(fr"TABLE_{table_name}_TITLE.*", i)]
        new_dict = {}
        for elem in form_errors_list:
            new_dict[elem] = getattr(page_locators, elem)

        return new_dict

    def filters_dict_generator(self, page_locators, table_name):
        """Генерирует словарь блоков фильтрации"""
        table_filter_list = [i for i in dir(page_locators) if
                            re.fullmatch(fr"FILTER_{table_name}_.*", i)]
        new_dict = {}
        for elem in table_filter_list:
            new_dict[elem] = getattr(page_locators, elem)

        return new_dict


    def form_using(self, form_dict: dict, data_dict: dict):
        """Работает с формой"""

        for form_elem in form_dict:
            if "INPUT" in form_elem:
                form_dict[form_elem].send_keys(data_dict[form_elem])
            elif 'RADIO' in form_elem:
                form_dict[form_elem].click()
            elif 'SELECT' in form_elem:
                try:
                    select = Select(form_dict[form_elem])
                    select.select_by_visible_text(data_dict[form_elem])
                except StaleElementReferenceException:
                    pass
            elif 'BTN_SUBMIT' in form_elem:
                btn = form_dict[form_elem]
        btn.click()

    def clean_form(self, form_dict):
        """Очищает поля формы"""
        for form_elem in form_dict:
            if "INPUT" in form_elem:
                form_dict[form_elem].clear()

    def form_is_hide(self, form_locator):
        """Проверка того, что форму не видно"""
        doc_form = self.browser.find_element(*form_locator)
        hide_class = 'data-show-or-hide-form'
        if hide_class in doc_form.get_attribute('class'):
                return True
        return False

    def count_checker(self, locator, check_count):
        """Проверяет кол-во < . . . >"""
        count = self.browser.find_element(*locator).text
        return count

    def go_back(self):
        """Возвращает на предыдущую стр."""
        self.browser.execute_script("window.history.go(-1)")

    def click_on_unclickable_element(self, element):
        """Клик по элементу на котором не работает метод .click()"""
        self.browser.execute_script("arguments[0].click();", element)

    def hover_element(self, element):
        """Наведение мыши на элемент"""
        hover = ActionChains(self.browser).move_to_element(element)
        hover.perform()

    def set_filters__conclusions(self, filters_dict: dict, conclusions_dict: dict):
        """Базовый метод установки условий фильтрации"""

        # Перевернем списки WebElement'ов
        # для корректного обращения по индексу
        for block in filters_dict:
            if type(filters_dict[block]) is list:
                filters_dict[block].reverse()
        # Перебираем ключи условий поиска и вводим их
        for c in conclusions_dict:
            if 'INPUT' in c:
                filters_dict[c].send_keys(
                    conclusions_dict[c]
                )
            elif 'CHECK' in c:
                # Получение ключа TITLE'а checkbox'ов
                c_title = c[0:-6] + "TITLE"
                # c = 'FILTER_CARS_BRANDS_CHECKS': (1)
                # наводим мышку на title
                self.hover_element(filters_dict[c_title])
                for check_index in conclusions_dict[c]:
                    check_boxes = filters_dict[c]
                    print(check_boxes)
                    click_elem = check_boxes[check_index]
                    # print(conclusions_dict[c])
                    # check_box = filters_dict[c][conclusions_dict[c][check_index]]
                    # Нажимаем на
                    self.click_on_unclickable_element(click_elem)