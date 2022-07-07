import time

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from cabinet.models import MyUser
from .base_page import BasePage
from .locators import CarsPageLocators, AccountPageLocators


class CarsPage(BasePage):
    """Стр. всех автомобилей """

    def should_be_cars_page(self):
        """Проверка того, что это стр. 'автомобили"""
        self.should_be__page('/cars/')

    def should_be_car_add_form(self):
        """Проверка наличия формы добавления авто"""
        self.reload()

        car_add_form_dict = self.should_be_the_form(CarsPageLocators, "CAR_ADD")

        # Проверяем, что форму НЕ видно
        if self.form_is_hide(CarsPageLocators.FORM_CAR_ADD_TITLE):
            assert False, "Форму видно до нажатия кнопки"

        # Нажимаем на кнопку открытия формы
        car_add_btn = self.browser.find_element(*CarsPageLocators.FORM_CAR_ADD_BTN_OPEN)
        car_add_btn.click()

        # Проверяем, что форму видно
        if not self.form_is_hide(CarsPageLocators.FORM_CAR_ADD_TITLE):
            assert False, "Форму Не видно ПОСЛЕ нажатия кнопки"

        return car_add_form_dict

    def add_car(self, car_dict, add_car_form):
        """Добавляет машину"""
        self.form_using(add_car_form, car_dict)

    def add_car_form_is_hide(self):
        if self.form_is_hide(
                CarsPageLocators.FORM_CAR_ADD_TITLE):
            assert False, "Форму видна!"
        else:
            assert True

    def add_car_form_is_NOT_hide(self):
        if self.form_is_hide(
                *CarsPageLocators.FORM_CAR_ADD_TITLE):
            assert False, "Форму не видно!!!"
        else:
            assert True

    def close_message_add_car_success(self):
        """Закрывает сообщение об успешном добавлении авто"""
        self.close_message(
            CarsPageLocators.FORM_ADD_CAR_MSG_SUCCESS_TEXT,
            CarsPageLocators.FORM_ADD_CAR_MSG_SUCCESS_CROSS
        )

    def should_be_cars_table(self):
        """Проверяет наличие таблицы 'cars'"""
        self.should_be_the_table(CarsPageLocators, 'CARS')

    def should_be_filtration_blocks(self):
        """Проверяет наличие блоков фильтрации"""
        return self.should_be_the_filter_blocks(CarsPageLocators, 'CARS')

    def should_NOT_be_cars_table(self):
        """Проверяет отсутствие  таблицы 'cars'"""
        if self.should_be_NOT_the_table(CarsPageLocators.INFO_NOT_CAR):
            assert True
        else:
            assert False, "Таблица машины на стр.!!!"

    def check_car_count(self, check_count):
        count = self.count_checker(CarsPageLocators.INFO_CAR_COUNT, check_count)
        if count != check_count:
            assert False, f"Кол-во машин на стр: {count} ." \
                          f"Вместо {check_count}"

    def go_to_car_page_by_table_row(self, reg_number):
        """Переход на запись выбранного авто"""
        reg_number = f"{reg_number[0:1]}-{reg_number[1:4]}-{reg_number[4:6]}"
        self.go_to__page_by_table_row('cars', reg_number)

    def go_to_driver_page_by_table_row(self, driver: MyUser):
        """Переход на запись выбранного авто"""
        driver = f"{driver.last_name} " \
                 f"{driver.first_name[0]}." \
                 f"{driver.patronymic[0]}."
        print(driver)
        self.go_to__page_by_table_row('cars', driver)

    def car_is_in_table(self, car):
        """Проверка наличия машины в таблице"""
        reg_number = f"{car.registration_number[0:1]}" \
                     f"-{car.registration_number[1:4]}" \
                     f"-{car.registration_number[4:6]}"

        if self.is_row_in_table('cars',reg_number):
            assert False, f"Машина {reg_number} не найдена!"

    def car_is_NOT_in_table(self, car):
        """Проверка наличия машины в таблице"""
        reg_number = f"{car.registration_number[0:1]}" \
                     f"-{car.registration_number[1:4]}" \
                     f"-{car.registration_number[4:6]}"
        if self.is_row_in_table('cars', reg_number):
            assert False, f"Машина {reg_number} НАЙДЕНА!"

    def delete_car(self, cars: list):
        """Удаление список машин"""

        # Получаем check_box выбранной машины
        for car in cars:
            try:
                delete_check = self.browser.find_element(By.CSS_SELECTOR, f"input[name='owner_delete_id'][value='{car.pk}']")
                delete_check.click()
            except:
                assert False, f"check-box удаления машины - {car.registration_number} не найден"

        # Нажимаем кнопку "удалить"
        delete_btn = self.browser.find_element(By.CSS_SELECTOR, "button.table__delete")
        delete_btn.click()

    def withdraw_car(self, cars: list):
        """Изымает список машин"""

        # Получаем check_box выбранной машины
        for car in cars:
            try:
                withdraw_check = self.browser.find_element(By.CSS_SELECTOR, f"input[name='owner_refuse_id'][value='{car.pk}']")
                withdraw_check.click()
            except:
                assert False, f"check-box изъятия машины - {car.registration_number} не найден"

        # Нажимаем кнопку "удалить"
        withdraw_btn = self.browser.find_element(By.CSS_SELECTOR, "button.table__confiscate")
        withdraw_btn.click()

    def car_is_refused(self, car):
        """Проверяет, что машина изъята"""

        # try:
        #     withdraw_check = self.browser.find_element(
        #         By.CSS_SELECTOR, f"input[name='owner_refuse_id'][value='{car.pk}']"
        #     )
        # except NoSuchElementException:
        #     assert True
        # assert False, f"Машина {car.registration_number} не изъята!!!"

        if self.is_element_present(By.CSS_SELECTOR, f"input[name='owner_refuse_id'][value='{car.pk}']"):
            assert False, f"Машина {car.registration_number} не изъята!!!"


    def set_filters_cars_conclusion(self, filter_blocks: dict, conclusions: dict):
        """Запускаем фильтрацию по переданным параметрам машины"""

        self.set_filters__conclusions(filter_blocks, conclusions)

        filter_blocks['FILTER_CARS_BTN_SUBMIT'].click()


    def check_filter_results(self, cars_list: list):
        """Проверяет результаты фильтрации"""

        count = str(len(cars_list))
        self.check_car_count(count)
        for car in cars_list:
            self.car_is_in_table(car)

    def reset_filter_result(self):
        """Нажимает кнопку сбросить"""

        try:
            reset_btn = self.browser.find_element(*CarsPageLocators.FILTER_CARS_BTN_RESET)
        except NoSuchElementException:
            assert False, "Кнопка сброса не найдена"

        reset_btn.click()