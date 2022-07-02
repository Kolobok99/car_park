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

    def should_be_the_(self, form_dict):
        """Проверка наличия элементов < формы, таблицы >"""
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


    def should_be_cars_table(self):
        form_dict = {
            'TABLE CAR TITLE': AccountPageLocators.TABLE_CARS_HEADER,
            'TABLE CAR REG NUMBER': AccountPageLocators.TABLE_CARS_TITLE_REG_NUMBER,
            'TABLE CAR BRAND': AccountPageLocators.TABLE_CARS_TITLE_BRAND,
            'TABLE CAR REGION CODE': AccountPageLocators.TABLE_CARS_TITLE_REGION_CODE,
            'TABLE CAR LAST INSPECTION': AccountPageLocators.TABLE_CARS_TITLE_LAST_INSPECTION,
            'TABLE CAR ACTIVE APPS': AccountPageLocators.TABLE_CARS_TITLE_ACTIVE_APPS,
        }
        car_table_form_dict = self.should_be_the_(form_dict)
        return car_table_form_dict

    def should_be_apps_table(self):
        form_dict = {
            'TABLE APP TITLE': AccountPageLocators.TABLE_APPS_HEADER,
            'TABLE APP ID': AccountPageLocators.TABLE_APPS_TITLE_APP_ID,
            'TABLE APP DATE': AccountPageLocators.TABLE_APPS_TITLE_DATE,
            'TABLE APP URGENCY': AccountPageLocators.TABLE_APPS_TITLE_URGENCY,
            'TABLE APP STATUS': AccountPageLocators.TABLE_APPS_TITLE_STATUS,
            'TABLE APP TYPE': AccountPageLocators.TABLE_APPS_TITLE_TYPE,
            'TABLE APP CAR': AccountPageLocators.TABLE_APPS_TITLE_CAR,
            'TABLE APP DESCRIPTION': AccountPageLocators.TABLE_APPS_TITLE_DESCRIPTION,
        }
        app_table_form_dict = self.should_be_the_(form_dict)
        return app_table_form_dict

    def should_be_cards_table(self):
        form_dict = {
            'TABLE CARD TITLE': AccountPageLocators.TABLE_CARS_HEADER,
            'TABLE CARD ID': AccountPageLocators.TABLE_CARS_TITLE_REG_NUMBER,
            'TABLE CARD NUMBER': AccountPageLocators.TABLE_CARS_TITLE_BRAND,
            'TABLE CARD LIMIT': AccountPageLocators.TABLE_CARS_TITLE_REGION_CODE,
            'TABLE CARD BALANCE': AccountPageLocators.TABLE_CARS_TITLE_LAST_INSPECTION,
            'TABLE CARD ACTIONS': AccountPageLocators.TABLE_CARS_TITLE_ACTIVE_APPS,
        }
        card_table_form_dict = self.should_be_the_(form_dict)
        return card_table_form_dict

    def should_be_docs_table(self):
        """Проверка наличия формы <Документы>"""

        form_dict = {
            'TABLE DOC TITLE': AccountPageLocators.TABLE_CARS_HEADER,
            'TABLE DOC TYPE': AccountPageLocators.TABLE_CARS_TITLE_REG_NUMBER,
            'TABLE DOC START DATE': AccountPageLocators.TABLE_CARS_TITLE_BRAND,
            'TABLE DOC END DATE': AccountPageLocators.TABLE_CARS_TITLE_REGION_CODE,
            'TABLE DOC LAST COPY': AccountPageLocators.TABLE_CARS_TITLE_LAST_INSPECTION,
            'TABLE DOC ACTIONS': AccountPageLocators.TABLE_CARS_TITLE_ACTIVE_APPS,
        }
        docs_table_form_dict = self.should_be_the_(form_dict)
        return docs_table_form_dict