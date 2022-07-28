import time

from selenium.webdriver.common.by import By

from car_park.settings import BASE_DIR
from selenium.common import NoSuchElementException

from cabinet.tests.end2end.pages.base_page import BasePage
from cabinet.tests.end2end.pages.locators import AccountPageLocators, HeaderLocators
from cabinet.tests.end2end.pages.login_page import LoginPage


class AccountPage(BasePage):

    def should_be_account_page(self):
        """Проверка того, что это стр. 'registration' """
        self.should_be__page('/account/')

    def should_be_form_to_change_data(self):
        """Проверка наличия формы авторизации"""
        personal_data_form_dict = self.should_be_the_form(AccountPageLocators, 'PERSONAL')
        return personal_data_form_dict

    def should_be_form_to_change_balance(self):
        """Проверка наличия формы изменения баланса карты"""
        change_balance_form_dict = self.should_be_the_form(AccountPageLocators, 'CARD_BALANCE')
        return change_balance_form_dict

    def should_be_doc_add_form(self):
        """Проверяем наличие формы добавления документа"""
        self.reload()

        docs_add_form_dict = self.should_be_the_form(AccountPageLocators, "DOC_ADD")

        # Проверяем, что форму НЕ видно
        if self.add_doc_form_is_hide():
            assert False, "Форму видно до нажатия кнопки"

        # Нажимаем на кнопку открытия формы
        add_doc_btn = self.browser.find_element(*AccountPageLocators.FORM_DOC_ADD_BTN_OPEN)
        add_doc_btn.click()

        # Проверяем, что форму видно
        if not self.add_doc_form_is_hide():
            assert False, "Форму Не видно ПОСЛЕ нажатия кнопки"

        return docs_add_form_dict



    def should_be_cars_table(self):
        """Проверяет наличие таблицы 'cars'"""
        self.should_be_the_table(AccountPageLocators, 'CARS')

    def should_be_apps_table(self):
        """Проверяет наличие таблицы 'apps'"""
        self.should_be_the_table(AccountPageLocators, 'APPS')

    def should_be_cards_table(self):
        """Проверяет наличие таблицы 'cards'"""
        self.should_be_the_table(AccountPageLocators, 'CARDS')

    def should_be_docs_table(self):
        """Проверяет наличие таблицы 'docs'"""
        self.should_be_the_table(AccountPageLocators, 'DOCS')


    def should_be_user_card(self, card_pk):
        """Проверяет наличие карты"""
        if not self.is_row_in_table('cards', card_pk):
            assert False, "Карта не найдена"



    def change_personal_data(self, change_data, form_dict):
        """Изменяет личные данные"""

        self.form_using(form_dict, change_data)

    def check_personal_data(self, check_data):
        """Проверяет персональные данные"""
        differences = {}
        change_form = self.should_be_form_to_change_data()
        keys = ['FORM_PERSONAL_INPUT_F_NAME',
                'FORM_PERSONAL_INPUT_L_NAME',
                'FORM_PERSONAL_INPUT_P_NAME',
                'FORM_PERSONAL_INPUT_PHONE']
        for key in keys:
            if check_data[key] != change_form[key].get_attribute('value'):
                differences[key] = f"Вместо {check_data[key]}, {change_form[key].text}"
        if differences:
            assert False, f"Несоответствия: {differences}"
        else:
            assert True



    def close_change_personal_data_success_message(self):
        """Метод закрытия сообщений об успешном изменении личных данных"""
        self.close_message(
            AccountPageLocators.FORM_PERSONAL_MSG_SUCCESS_TEXT,
            AccountPageLocators.FORM_PERSONAL_MSG_SUCCESS_CROSS
        )
        # try:
        #     message = self.is_element_present(*AccountPageLocators.FORM_PERSONAL_MSG_SUCCESS_TEXT)
        # except NoSuchElementException:
        #     assert False, "Сообщение не найдено!"
        #
        # try:
        #     msg_cross = self.browser.find_element(*AccountPageLocators.FORM_PERSONAL_MSG_SUCCESS_CROSS)
        #     msg_cross.click()
        # except NoSuchElementException:
        #     assert False, "Крестик не найден"
        #
        # try:
        #     self.is_not_element_present(*AccountPageLocators.FORM_PERSONAL_MSG_SUCCESS_TEXT)
        # except NoSuchElementException:
        #     assert False, "Сообщение не исчезло после закрытия"

    def close_change_balance_msg(self):
        """Закрывает сообщение об успешном смене баланса"""
        self.close_message(
            AccountPageLocators.FORM_CARD_BALANCE_MSG_SUCCESS_TEXT,
            AccountPageLocators.FORM_CARD_BALANCE_MSG_SUCCESS_CROSS
        )

    def close_message_delete_doc_success(self):
        """Закрывает сообщение об успешном удалении документа"""
        self.close_message(
            AccountPageLocators.FORM_DOC_DELETE_MSG_SUCCESS_TITLE,
            AccountPageLocators.FORM_ADD_DOC_MSG_SUCCESS_CROSS
        )

    def close_message_add_doc_success(self):
        """Закрывает сообщение об успешном добавлении документа"""
        self.close_message(
            AccountPageLocators.FORM_ADD_DOC_MSG_SUCCESS_TEXT,
            AccountPageLocators.FORM_ADD_DOC_MSG_SUCCESS_CROSS
        )


    def change_card_balance(self, balance_data, form_dict):
        """Изменяет баланс карты"""
        self.form_using(form_dict, balance_data)

    def check_balance(self, balance):
        """Проверяет, что баланс карты, равен переданному балансу"""

        balance_input = self.browser.find_element(*AccountPageLocators.FORM_CARD_BALANCE_INPUT_BALANCE)

        if balance_input.get_attribute('value') != balance:
            assert False, \
                f"Баланс равен {balance_input.get_attribute('value')}" \
                 f"Вместо {balance}"






    def add_doc_form_is_hide(self):
        """Проверка того, что форму
         добавления дока не видно"""
        doc_form = self.browser.find_element(*AccountPageLocators.FORM_DOC_ADD_TITLE)
        hide_class = 'data-show-or-hide-form'
        if hide_class in doc_form.get_attribute('class'):
            return True
        return False

    def add_doc_form_is_NOT_hide(self):
        """Проверка того, что форму
         добавления дока не видно"""
        doc_form = self.browser.find_element(*AccountPageLocators.FORM_DOC_ADD_TITLE)
        hide_class = 'data-show-or-hide-form'
        if hide_class in doc_form.get_attribute('class'):
            return False
        return True

    def confirm_delete_form_is_hide(self):
        """Проверка того, что форму
         подтверждения не видно"""
        confirm_delete_form = self.browser.find_element(*AccountPageLocators.DELETE_DOC_CONFIRM_DELETE)
        hide_class = 'data-show-or-hide-form'
        if hide_class in confirm_delete_form.get_attribute('class'):
            return True
        return False

    def delete_doc_btn_finder(self, id):
        """Возвращает кнопку удаления заявки"""

        delete_btn = self.browser.find_element(By.CSS_SELECTOR, f"button.table__btn-delete-app[id='doc-{id}']")

        return delete_btn

    def add_doc(self, doc_data, form_dict):
        """Добавление документа"""

        self.form_using(form_dict, doc_data)

    def is_doc_in_table(self, type, start_date, end_date):
        """Проверка наличия документа в таблице"""
        self.is_row_in_table('docs', start_date)
        self.is_row_in_table('docs', end_date)
        self.is_row_in_table('docs', type)

    def delete_doc(self, id):
        """Удаление документа"""
        #Нажимаем кнопку "Удалить"
        delete_doc_btn = self.delete_doc_btn_finder(id)
        delete_doc_btn.click()

        # Подтверждаем удаление документа
        yes_delete_btn = self.browser.find_element(*AccountPageLocators.FORM_DOC_DELETE_BTN_SUBMIT)
        yes_delete_btn.click()

    def has_error(self):
        """Проверяет появилось ли сообщение об ошибке"""

        self.is_element_present(*AccountPageLocators.FORM_DOC_ADD_ERROR_DATE)



    def go_to_cars_page_by_btn(self):
        """Переход на стр. 'cars' """

        self.go_to__page_by_btn(HeaderLocators.LINK_BTN_CARS, 'машины')