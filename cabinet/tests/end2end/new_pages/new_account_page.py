import time

from selenium.webdriver.common.by import By

from car_park.settings import BASE_DIR
from selenium.common import NoSuchElementException

from cabinet.tests.end2end.new_pages.new_base_page import BasePage
from cabinet.tests.end2end.new_pages.new_locators import AccountPageLocators, HeaderLocators
from cabinet.tests.end2end.new_pages.new_login_page import LoginPage


class AccountPage(BasePage):

    def should_be_account_page(self):
        """Проверка того, что это стр. 'registration' """
        self.should_be__page('/account/')

    def should_be_form_to_change_data(self):
        """Проверка наличия формы авторизации"""
        form_dict = {
            'FIRST NAME': AccountPageLocators.FORM_PERSONAL_INPUT_F_NAME,
            'LAST NAME': AccountPageLocators.FORM_PERSONAL_INPUT_L_NAME,
            'PATRONYMIC': AccountPageLocators.FORM_PERSONAL_INPUT_P_NAME,
            'FORM_PERSONAL_INPUT_PHONE': AccountPageLocators.PHONE_INPUT,
            'EMAIL': AccountPageLocators.FORM_PERSONAL_INPUT_EMAIL,
            'BUTTON SUBMIT': AccountPageLocators.FORM_PERSONAL_BTN_SUBMIT,
        }
        change_personal_data_form_dict = self.should_be_the_(form_dict)
        return change_personal_data_form_dict

    def change_personal_data(self, change_data, form_data):
        """Изменяет личные данные"""

        form_data['FIRST NAME'].clear()
        form_data['FIRST NAME'].send_keys(change_data['FIRST NAME'])

        form_data['LAST NAME'].clear()
        form_data['LAST NAME'].send_keys(change_data['LAST NAME'])

        form_data['PATRONYMIC'].clear()
        form_data['PATRONYMIC'].send_keys(change_data['PATRONYMIC'])

        form_data['FORM_PERSONAL_INPUT_PHONE'].clear()
        form_data['FORM_PERSONAL_INPUT_PHONE'].send_keys(change_data['FORM_PERSONAL_INPUT_PHONE'])

        form_data['BUTTON SUBMIT'].click()

    def check_personal_data(self, check_data):
        """Проверяет персональные данные"""
        differences = {}
        change_form = self.should_be_form_to_change_data()
        keys = ['FIRST NAME', 'LAST NAME', 'PATRONYMIC', 'FORM_PERSONAL_INPUT_PHONE']
        for key in keys:
            if check_data[key] != change_form[key].get_attribute('value'):
                differences[key] = f"Вместо {check_data[key]}, {change_form[key].text}"
        if differences:
            assert False, f"Несоответствия: {differences}"
        else:
            assert True

    def close_change_personal_data_success_message(self):
        """Метод закрытия сообщений об успешном изменении личных данных"""

        try:
            message = self.is_element_present(*AccountPageLocators.CHANGE_DATA_SUCCESS_MSG)
        except NoSuchElementException:
            assert False, "Сообщение не найдено!"

        try:
            msg_cross = self.browser.find_element(*AccountPageLocators.CHANGE_DATA_SUCCESS_CROSS)
            msg_cross.click()
        except NoSuchElementException:
            assert False, "Крестик не найден"

        try:
            self.is_not_element_present(*AccountPageLocators.CHANGE_DATA_SUCCESS_MSG)
        except NoSuchElementException:
            assert False, "Сообщение не исчезло после закрытия"

    def close_change_balance_msg(self):
        """Закрывает сообщение об успешном смене баланса"""
        self.close_message(
            AccountPageLocators.CHANGE_BALANCE_SUCCESS_MSG,
            AccountPageLocators.CHANGE_DATA_SUCCESS_CROSS
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

    def should_be_user_card(self, card_pk):
        """Проверяет наличие карты"""
        if not self.is_row_in_table('cards', card_pk):
            assert False, "Карта не найдена"

    def check_balance(self, balance):
        """Проверяет, что баланс карты, равен переданному балансу"""

        balance_input = self.browser.find_element(*AccountPageLocators.FORM_CARD_BALANCE_INPUT_BALANCE)

        if balance_input.get_attribute('value') != balance:
            assert False, \
                f"Баланс равен {balance_input.get_attribute('value')}" \
                 f"Вместо {balance}"

    def change_card_balance(self, new_balance: str):
        """Изменяет баланс карты"""
        # Пытаемся
        try:
            balance_input = self.browser.find_element(*AccountPageLocators.FORM_CARD_BALANCE_INPUT_BALANCE)
            balance_btn = self.browser.find_element(*AccountPageLocators.TABLE_ROW_BALANCE_BTN)
        except NoSuchElementException:
            assert False, "Не найдены эл. изменения баланса"

        balance_input.clear()
        balance_input.send_keys(new_balance)
        time.sleep(5)
        balance_btn.click()

    # def should_be_docs_table(self):
    #     """Проверяем наличие формы авторизации"""
    #
    #     table_dict = {
    #         'TABLE DOC TITLE': AccountPageLocators.TABLE_CARS_HEADER,
    #         'TABLE DOC TYPE': AccountPageLocators.TABLE_CARS_TITLE_REG_NUMBER,
    #         'TABLE DOC START DATE': AccountPageLocators.TABLE_CARS_TITLE_BRAND,
    #         'TABLE DOC END DATE': AccountPageLocators.TABLE_CARS_TITLE_REGION_CODE,
    #         'TABLE DOC LAST COPY': AccountPageLocators.TABLE_CARS_TITLE_LAST_INSPECTION,
    #         'TABLE DOC ACTIONS': AccountPageLocators.TABLE_CARS_TITLE_ACTIVE_APPS,
    #     }
    #     docs_table_dict = self.should_be_the_(table_dict)
    #     return docs_table_dict

    def should_be_doc_add_form(self):
        """Проверяем наличие формы добавления документа"""
        self.reload()

        # Проверяем, что форма находится на стр.
        form_dict = {
            'DOC ADD BTN': AccountPageLocators.FORM_DOC_ADD_BTN_OPEN,
            'DOC TYPE RADIO': AccountPageLocators.FORM_DOC_ADD_RADIO_TYPE,
            'DOC START DATE INPUT': AccountPageLocators.FORM_DOC_ADD_INPUT_START_DATE,
            'DOC END DATE INPUT': AccountPageLocators.FORM_DOC_ADD_INPUT_END_DATE,
            'DOC COPY INPUT': AccountPageLocators.FORM_DOC_ADD_INPUT_COPY,
            'DOC SUBMIT BTN': AccountPageLocators.FORM_DOC_ADD_BTN_SUBMIT,
            'DOC CLOSE FORM BTN': AccountPageLocators.FORM_DOC_ADD_RESET
        }
        docs_add_form_dict = self.should_be_the_(form_dict)

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
    def add_user_doc(self, doc_dict, add_doc_form):
        """Добавление документа"""

        # ВВодим данные, нажимаем кнопку Отправить
        doc_path = str(BASE_DIR) + '/cabinet/tests/test_files/Instruction.pdf'
        add_doc_form['DOC TYPE RADIO'].click()
        add_doc_form['DOC START DATE INPUT'].send_keys(doc_dict['start_date'])
        add_doc_form['DOC END DATE INPUT'].send_keys(doc_dict['end_date'])
        add_doc_form['DOC COPY INPUT'].send_keys(doc_path)
        add_doc_form['DOC SUBMIT BTN'].click()

        # Проверяем, что форму НЕ видно
        if self.add_doc_form_is_hide():
            assert False, "Форму видно после загрузки документа"

        # Закрываем сообщение
        self.close_message(
            AccountPageLocators.FORM_ADD_DOC_MSG_SUCCESS_TEXT,
            AccountPageLocators.FORM_ADD_DOC_MSG_SUCCESS_CROSS
        )

        # Проверяем, что документ появился
        self.is_row_in_table('docs', "10-10-2021")
        self.is_row_in_table('docs', "21-12-2022")
        self.is_row_in_table('docs', "паспорт")

        # Получаем кнопку удаления дока
        delete_doc_btn = self.delete_doc_btn_finder(1)
        delete_doc_btn.click()

        # Проверяем появление формы удаления

        # Проверяем, что форму НЕ видно
        if not self.confirm_delete_form_is_hide():
            assert False, "Форма подтверждения удаления дока не появилась"

        # Подтверждаем удаление документа

        yes_delete_btn = self.browser.find_element(*AccountPageLocators.FORM_DOC_DELETE_BTN_SUBMIT)
        yes_delete_btn.click()
        # time.sleep(10)

        self.close_message(
            AccountPageLocators.FORM_DOC_DELETE_MSG_SUCCESS_TITLE,
            AccountPageLocators.FORM_ADD_DOC_MSG_SUCCESS_CROSS
        )

        if self.is_row_in_table('docs', "10-10-2021"):
            assert False, "Документ не удалился"

    def add_doc(self, doc_dict, add_doc_form):
        """Добавление документа"""

        # Путь к тестовому документу
        doc_path = str(BASE_DIR) + '/cabinet/tests/test_files/Instruction.pdf'

        # Открываем форму
        add_doc_form['DOC TYPE RADIO'].click()
        # Заполняем ее
        add_doc_form['DOC START DATE INPUT'].send_keys(doc_dict['start_date'])
        add_doc_form['DOC END DATE INPUT'].send_keys(doc_dict['end_date'])
        add_doc_form['DOC COPY INPUT'].send_keys(doc_path)

        # Нажимаем кнопку "Отправить"
        add_doc_form['DOC SUBMIT BTN'].click()

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

        self.is_element_present(*AccountPageLocators.DOC_DATE_ERROR)

