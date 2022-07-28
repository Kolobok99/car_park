import time

import pytest
from django.test import override_settings
from cabinet.models import MyUser, CarBrand, Car, Application, TypeOfAppl
from cabinet.tests.end2end.pages.account_page import AccountPage
from cabinet.tests.end2end.pages.car_page import CarPage
from cabinet.tests.end2end.pages.cars_page import CarsPage
from cabinet.tests.end2end.pages.driver_page import DriverPage
from cabinet.tests.end2end.pages.reg_page import RegistrationPage
from cabinet.tests.end2end.pages.login_page import LoginPage

LINK = "/cars"
class TestCarsPage:

    def manager_login(self, browser, live_server, create_user):
        """Инициализация объекта 'Аккаунт (авторизация менеджера)'"""
        page = LoginPage(browser, live_server.url)
        page.open()
        login_form = page.should_be_sign_in_form()
        test_manager, manager_pass = create_user(role='m')
        login_data = {
            'FORM_LOGIN_INPUT_EMAIL': test_manager.email,
            'FORM_LOGIN_INPUT_PASSWORD': manager_pass,
        }
        page.user_sign_in(login_data, login_form)

        account_page = AccountPage(browser, browser.current_url)
        account_page.go_to_cars_page_by_btn()
        # Инициализация объекта "Регистрация"
        cars_page = CarsPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/registration"
        return cars_page


    # @pytest.mark.skip
    def test_this_is_cars_page(self, browser, live_server, create_user):
        """Тест: это стр. 'автомобили'?"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_be_cars_page()

    @pytest.mark.django_db
    @override_settings(DEBUG=True)
    def test_manager_can_add_new_car_with_valid_data(self, browser, live_server, create_user):
        """Тест: добавление новых машин:
                1) Машины без водителя
                2) Машину с водителем
        """
        # Инициализируем объект 'Машины'
        page = self.manager_login(browser, live_server, create_user)

        # Добавляем новую марку 'TOYOTA', 'KIA'
        brands_list = ['TOYOTA_1', 'KIA_2']
        for brand in brands_list:
            CarBrand.objects.create(
                title=brand[0:-2]
            )

        # Получаем форму добавления авто
        add_car_form = page.should_be_car_add_form()
        # Инициализируем данные для создания авто (без водителя)
        reg_number_1 = 'A999AA'
        car_dict_1 = {
            'FORM_CAR_ADD_INPUT_REG_NUMBER': reg_number_1,
            'FORM_CAR_ADD_SELECT_BRAND': 'KIA',
            'FORM_CAR_ADD_INPUT_REGION': '86',
            'FORM_CAR_ADD_INPUT_LAST_INSPECTION': '12-12-2021',
            'FORM_CAR_ADD_SELECT_DRIVER': 'не выбран',
        }
        # Открываем форму добавления авто,
        # заполняем ее нажимаем кнопку отправить
        page.add_car(car_dict_1, add_car_form)

        # Форма исчезла
        page.add_car_form_is_hide()

        # Закрываем сообщение "Машина добавлена!"
        page.close_message_add_car_success()

        # проверяем кол-во отображаемых машин
        page.check_car_count("1")

        # Пытаемся перейти на стр. авто
        page.go_to_car_page_by_table_row(reg_number_1)

        # Инициализация объекта авто
        new_car_page = CarPage(browser, browser.current_url)

        # Проверяем, что мы на стр. выбранного авто
        new_car_page.should_be__page(reg_number_1)

        # Возвращаемся на стр. "Машины"
        new_car_page.go_to_cars_page_by_btn()
        page = CarsPage(browser, browser.current_url)

        # Создаем нового водителя
        # test_manager = MyUser.objects.get(role='m')
        MyUser.objects.create_user(
            email="test_driver@mail.com",
            password='12345',
            first_name="Петр",
            last_name="Петров",
            patronymic="Иванович",
            phone=89887656780,
            role='d',
            is_active=True,

        )
        page.reload()

        # Получаем форму добавления авто
        add_car_form = page.should_be_car_add_form()

        new_driver = MyUser.objects.get(email='test_driver@mail.com')
        # Инициализируем данные для создания авто (с водителем)
        reg_number_2 = 'B999BB'
        car_dict_2 = {
            'FORM_CAR_ADD_INPUT_REG_NUMBER': reg_number_2,
            'FORM_CAR_ADD_SELECT_BRAND': 'KIA',
            'FORM_CAR_ADD_INPUT_REGION': '86',
            'FORM_CAR_ADD_INPUT_LAST_INSPECTION': '10-11-2021',
            'FORM_CAR_ADD_SELECT_DRIVER':
                f'{new_driver.first_name} {new_driver.last_name}',
        }
        # Открываем форму добавления авто,
        # заполняем ее нажимаем кнопку отправить
        page.add_car(car_dict_2, add_car_form)

        # Форма исчезла
        page.add_car_form_is_hide()

        # Закрываем сообщение "Машина добавлена!"
        page.close_message_add_car_success()

        # проверяем кол-во отображаемых машин
        page.check_car_count("2")

        # Пытаемся перейти на стр. водителя (менеджера)
        page.go_to_driver_page_by_table_row(new_driver)

        # Инициализация объекта водитель
        driver_page = DriverPage(browser, browser.current_url)

        # Проверяем, что мы на стр. выбранного водителя
        driver_page.should_be_driver_page(new_driver)

        # Возвращаемся на стр. "Машины"
        new_car_page.go_to_cars_page_by_btn()
        page = CarsPage(browser, browser.current_url)

        # Удаляем созданные машины
        new_cars = Car.objects.all().delete()

    @pytest.mark.django_db
    def test_manager_see_filtration_blocks(self, browser, live_server, create_user):
        """Тест: менеджер видит блок фильтрации"""
        page = self.manager_login(browser, live_server, create_user)
        # Добавляем новую марку 'TOYOTA', 'KIA'
        brands_list = ['TOYOTA_1', 'KIA_2']
        for brand in brands_list:
            CarBrand.objects.create(
                title=brand[0:-2]
            )

        # Добавим машину
        Car.objects.create(
            registration_number='A111AA',
            region_code='123',
            brand=CarBrand.objects.get(title='TOYOTA'),
            last_inspection='2021-12-12',

        )

        # Добавим тип заявки
        TypeOfAppl.objects.create(
            title='Плановый осмотр'
        )
        page.reload()
        page.should_be_filtration_blocks()

        # Удаляем созданные машины
        new_cars = Car.objects.all().delete()

    @pytest.mark.django_db
    def test_manager_see_cars_table(self, browser, live_server, create_user):
        """Тест: менеджер видит таблицу машин"""
        page = self.manager_login(browser, live_server, create_user)
        page.should_NOT_be_cars_table()

        # Добавляем бренд
        CarBrand.objects.create(
            title='TOYOTA'
        )
        # Добавляем авто
        Car.objects.create(
            registration_number='A111AA',
            region_code='123',
            brand=CarBrand.objects.get(title='TOYOTA'),
            last_inspection='2021-12-12',

        )
        # Проверяем, что таблица появилась
        page.reload()
        page.should_be_cars_page()
        Car.objects.all().delete()



    # @pytest.mark.django_db
    # @override_settings(DEBUG=True)
    # def test_reg_number_filter(self, browser, live_server, create_user):
    #     # Инициализируем объект 'машины'
    #     page = self.manager_login(browser, live_server, create_user)
    #
    #     # Получаем объект менеджера
    #     test_manager = MyUser.objects.get(role='m')
    #
    #     # Получаем блоки фильтрации
    #     filtration_blocks = page.should_be_filtration_blocks()
    #
    #     conclusion_1 = {
    #         'FILTER_CARS_REG_NUMBER_INPUT': 'A',
    #     }
    #     page.set_filters_cars_conclusion(filtration_blocks, conclusion_1)
    #     time.sleep(30)
    #     page.check_filter_results([cars_dict['car_0'],
    #                                cars_dict['car_2'],
    #                                cars_dict['car_4']])

    @pytest.mark.django_db
    @override_settings(DEBUG=True)
    def test_manager_filter_cars(self, browser, live_server, create_user):
        """Тест: менеджер проверяет работоспособность фильтра машин"""

        # Инициализируем объект 'машины'
        page = self.manager_login(browser, live_server, create_user)

        # Получаем объект менеджера
        test_manager = MyUser.objects.get(role='m')


        # Создаем марки TOYOTA и KIA
        brands_list = ['TOYOTA_1', 'KIA_2']
        for brand in brands_list:
            CarBrand.objects.create(
                title=brand[0:-2]
            )
        # Создаем типы заявок
        app_types_list = ['СТО_1', 'Осмотр_2']
        for app_type in app_types_list:
            TypeOfAppl.objects.create(
                title=app_type[0:-2]
            )

        # Создаем данные для проверки фильтрации
        reg_numbers = [
            'A123AA',
            'A119AD',
            'B134DD',
            'C186PL',
            'C135PF',
            'G119LO',
        ]
        brands = [
            CarBrand.objects.get(title='TOYOTA'),
            CarBrand.objects.get(title='KIA'),
            CarBrand.objects.get(title='TOYOTA'),
            CarBrand.objects.get(title='KIA'),
            CarBrand.objects.get(title='TOYOTA'),
            CarBrand.objects.get(title='KIA')
        ]
        region_codes = [
            '86',
            '86',
            '111',
            '111',
            '97',
            '86'
        ]
        last_inspections = [
            '2021-12-12',
            '2021-12-12',
            '2021-12-12',
            '2021-12-12',
            '2021-12-12',
            '2021-12-12',
        ]
        owners = [
            None,
            test_manager,
            None,
            test_manager,
            None,
            test_manager
        ]
        cars_dict = {}
        for indx in range(6):
            cars_dict[f'car_{indx}'] = Car.objects.create(
                registration_number=reg_numbers[indx],
                brand=brands[indx],
                region_code=region_codes[indx],
                last_inspection=last_inspections[indx],
                owner=owners[indx]
            )
        page.reload()

        # Проверяем кол-во отображаемых машин
        page.check_car_count("6")

        # Добавляем новые заявки
        Application.objects.create(
            type=TypeOfAppl.objects.get(title='СТО'),
            owner=test_manager,
            status='O',
            car=Car.objects.get(registration_number='A123AA'),
        )
        Application.objects.create(
            type=TypeOfAppl.objects.get(title='Осмотр'),
            owner=test_manager,
            status='O',
            car=Car.objects.get(registration_number='A123AA'),
        )
        Application.objects.create(
            type=TypeOfAppl.objects.get(title='СТО'),
            owner=test_manager,
            status='O',
            car=Car.objects.get(registration_number='A119AD'),
        )


        # ТЕСТ № 1
        # BRAND - (0) - TOYOTA
        # Ожидаем результат: car_0, car_2, car_4
        #
        # Получаем блоки фильтрации
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_1 = {
            'FILTER_CARS_BRANDS_CHECKS': (0,)
        }

        page.set_filters_cars_conclusion(filtration_blocks, conclusion_1)
        time.sleep(30)
        page.check_filter_results([cars_dict['car_0'],
                                   cars_dict['car_2'],
                                   cars_dict['car_4']])

        page.reset_filter_result()
        # ТЕСТ № 2
        # BRAND - (1) - KIA
        # Ожидаем результат: car_1, car_3, car_5

        # Получаем блоки фильтрации
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_2 = {
            # 'FILTER_CARS_REG_NUMBER_INPUT': '12',
            'FILTER_CARS_BRANDS_CHECKS': (1,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_2)
        page.check_filter_results([cars_dict['car_1'],
                                   cars_dict['car_3'],
                                   cars_dict['car_5']])
        page.reset_filter_result()
        # ТЕСТ № 3
        # BRAND - (0,1) - TOYOTA, KIA
        # Ожидаем результат: car_1, car_2, car_3, car_4, car_5, car_6

        # Получаем блоки фильтрации
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_3 = {
            # 'FILTER_CARS_REG_NUMBER_INPUT': '12',
            'FILTER_CARS_BRANDS_CHECKS': (0, 1)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_3)
        page.check_filter_results([cars_dict['car_0'],
                                   cars_dict['car_1'],
                                   cars_dict['car_2'],
                                   cars_dict['car_3'],
                                   cars_dict['car_4'],
                                   cars_dict['car_5'],
                                   ])

        # ТЕСТ № 4
        # REG_NUMBER - 'A'
        # Ожидаем результат: car_0, car_1,

        # Получаем блоки фильтрации
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_4 = {
            'FILTER_CARS_REG_NUMBER_INPUT': 'A',
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_4)
        page.check_filter_results([cars_dict['car_0'],
                                   cars_dict['car_1'],
                                   ])
        page.reset_filter_result()
        # ТЕСТ № 5
        # REG_NUMBER - '11'
        # Ожидаем результат: car_1, car_5,
        # Получаем блоки фильтрации
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_5 = {
            'FILTER_CARS_REG_NUMBER_INPUT': '11',
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_5)
        page.check_filter_results([cars_dict['car_1'],
                                   cars_dict['car_5'],
                                   ])
        page.reset_filter_result()

        # ТЕСТ № 6
        # REG_NUMBER - '4D'
        # Ожидаем результат: car_0, car_1,
        # Получаем блоки фильтрации
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_6 = {
            'FILTER_CARS_REG_NUMBER_INPUT': '4D',
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_6)
        page.check_filter_results([cars_dict['car_2'],
                                   ])
        page.reset_filter_result()
        # ТЕСТ № 7
        # DRIVER - YES (0)
        # Ожидаем результат: car_0, car_2, car_4
        # Получаем блоки фильтрации
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_7 = {
            'FILTER_CARS_HAS_DRIVER_CHECKS': (0,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_7)
        page.check_filter_results([cars_dict['car_0'],
                                   cars_dict['car_2'],
                                   cars_dict['car_4'],
                                   ])
        page.reset_filter_result()
        # ТЕСТ № 8
        # DRIVER - NO (1,)
        # Ожидаем результат: car_1, car_3, car_5
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_8 = {
            'FILTER_CARS_HAS_DRIVER_CHECKS': (1,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_8)
        page.check_filter_results([cars_dict['car_1'],
                                   cars_dict['car_3'],
                                   cars_dict['car_5'],
                                   ])
        page.reset_filter_result()
        # ТЕСТ № 9
        # REGION_CODE - 86 (2,)
        # Ожидаем результат: car_0, car_1, car_5
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_9 = {
            'FILTER_CARS_REGIONS_CHECKS': (2,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_9)
        page.check_filter_results([cars_dict['car_0'],
                                   cars_dict['car_1'],
                                   cars_dict['car_5'],
                                   ])
        page.reset_filter_result()
        # ТЕСТ № 10
        # REGION_CODE - 97
        # Ожидаем результат: car_4
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_10 = {
            'FILTER_CARS_REGIONS_CHECKS': (0,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_10)
        page.check_filter_results([cars_dict['car_4'],
                                   ])
        page.reset_filter_result()
        # ТЕСТ № 11
        # APP_TYPE - 0 (СТО)
        # Ожидаем результат: car_0, car_1
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_11 = {
            'FILTER_CARS_APP_TYPES_CHECKS': (1,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_11)
        page.check_filter_results([cars_dict['car_0'],
                                   cars_dict['car_1'],
                                   ])
        page.reset_filter_result()

        # ТЕСТ № 12
        # APP_TYPE - 1 (Осмотр)
        # Ожидаем результат: car_0
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_12 = {
            'FILTER_CARS_APP_TYPES_CHECKS': (0,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_12)
        page.check_filter_results([cars_dict['car_0'],
                                   ])
        page.reset_filter_result()

        # ТЕСТ № 13
        # REG_NUMBER - 'A'
        # Ожидаем результат: car_0
        filtration_blocks = page.should_be_filtration_blocks()

        conclusion_12 = {
            'FILTER_CARS_APP_TYPES_CHECKS': (0,)
        }
        page.set_filters_cars_conclusion(filtration_blocks, conclusion_12)
        page.check_filter_results([cars_dict['car_0'],
                                   ])
        page.reset_filter_result()

        Car.objects.all().delete()

    @pytest.mark.django_db
    @override_settings(DEBUG=True)
    def test_manager_can_withdraw_cars(self, browser, live_server, create_user):
        """Тест: менеджер может изъять список машиин"""

        page = self.manager_login(browser, live_server, create_user)


        # Добавляем новую марку 'TOYOTA', 'KIA'
        brands_list = ['TOYOTA_1', 'KIA_2']
        for brand in brands_list:
            CarBrand.objects.create(
                title=brand[0:-2]
            )
        # Получаем менеджер
        test_manager = MyUser.objects.get(role='m')
        # Создаем 3 новых машины
        new_car1 = Car.objects.create(
            registration_number='A111AA',
            brand=CarBrand.objects.get(title='TOYOTA'),
            region_code='123',
            last_inspection='2021-12-01',
            owner=test_manager,
        )
        new_car2 = Car.objects.create(
            registration_number='A222AA',
            brand=CarBrand.objects.get(title='KIA'),
            region_code='123',
            last_inspection='2021-12-02',
            owner=test_manager,
        )
        new_car3 = Car.objects.create(
            registration_number='A333AA',
            brand=CarBrand.objects.get(title='TOYOTA'),
            region_code='123',
            last_inspection='2021-12-03',
            owner=test_manager,
        )

        # Перезагружаем стр.
        page.reload()

        # проверяем кол-во отображаемых машин
        page.check_car_count("3")

        # Проверяем, что появились созданные машины
        page.car_is_in_table(new_car1)
        page.car_is_in_table(new_car2)
        page.car_is_in_table(new_car3)


        page.withdraw_car([new_car3])

        page.go_back()

        page.car_is_in_table(new_car1)
        page.car_is_in_table(new_car2)
        page.car_is_in_table(new_car3)

        page.car_is_refused(new_car3)
        # Удаляем созданные машины
        new_cars = Car.objects.all().delete()


    @pytest.mark.django_db
    @override_settings(DEBUG=True)
    def test_manager_can_delete_cars(self, browser, live_server, create_user):
        """Тест: менеджер может удалить список машиин"""

        page = self.manager_login(browser, live_server, create_user)


        # Добавляем новую марку 'TOYOTA', 'KIA'
        brands_list = ['TOYOTA_1', 'KIA_2']
        for brand in brands_list:
            CarBrand.objects.create(
                title=brand[0:-2]
            )
        # Получаем менеджер
        test_manager = MyUser.objects.get(role='m')
        # Создаем 3 новых машины
        new_car1 = Car.objects.create(
            registration_number='A111AA',
            brand=CarBrand.objects.get(title='TOYOTA'),
            region_code='123',
            last_inspection='2021-12-01',
            owner=test_manager,
        )
        new_car2 = Car.objects.create(
            registration_number='A222AA',
            brand=CarBrand.objects.get(title='KIA'),
            region_code='123',
            last_inspection='2021-12-02',
            owner=test_manager,
        )
        new_car3 = Car.objects.create(
            registration_number='A333AA',
            brand=CarBrand.objects.get(title='TOYOTA'),
            region_code='123',
            last_inspection='2021-12-03',
            owner=test_manager,
        )

        # Перезагружаем стр.
        page.reload()

        # проверяем кол-во отображаемых машин
        page.check_car_count("3")

        # Проверяем, что появились созданные машины
        page.car_is_in_table(new_car1)
        page.car_is_in_table(new_car2)
        page.car_is_in_table(new_car3)


        page.delete_car([new_car3])
        page.go_back()

        # проверяем кол-во отображаемых машин
        page.check_car_count("2")

        page.car_is_in_table(new_car1)
        page.car_is_in_table(new_car2)
        page.car_is_NOT_in_table(new_car3)

        # Удаляем созданные машины
        new_cars = Car.objects.all().delete()
