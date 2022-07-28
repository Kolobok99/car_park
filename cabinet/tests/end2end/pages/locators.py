from selenium.webdriver.common.by import By


# КНОПКА ССЫЛКИ             - LINK_BTN_<NAME>
# ИДЕНИТИФИКАЦИЯ СТР.       - <PAGE>_PAGE_NAME
# ИНФОРМАЦИЯ                - INFO_<INFO_NAME>
#
# FORM:
#       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
#       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
#       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
#       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
#       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
#       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
#       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
#       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
#
# MESSAGE:
#           TEXT            - FORM_<FORM_NAME>_MSG_<MSG_NAME>_TEXT
#           CROSS           - FORM_<FORM_NAME>_MSG_<MSG_NAME>_CROSS
#
# TABLE:
#       HEADER              - TABLE_<TABLE_NAME>_HEADER
#       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
#
# FILTERS:
#       УСЛОВИЕ             - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<TITLE>
#       ВАРИАНТ_УСЛОВИЕ     - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<CONDITION>
#       КНОПКА УСЛОВИЯ      - FILTER_<FILTER_NAME>_BTN_SUBMIT
#       СБРОС УСЛОВИЙ       - FILTER_<FILTER_NAME>_BTN_RESET


class Tables:

    # таблица "автомобили"
    TABLE_CARS_HEADER = (By.CSS_SELECTOR, ".cars > .table__table-title")

    TABLE_CARS_TITLE_REG_NUMBER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Номер']")
    TABLE_CARS_TITLE_BRAND = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Марка']")
    TABLE_CARS_TITLE_REGION_CODE = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Регион']")
    TABLE_CARS_TITLE_LAST_INSPECTION = (By.XPATH, "//*[contains(@class,'table__title')]//span[text() = 'Последний']")
    TTABLE_CARS_TITLE_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'table__title')]//span[text() = 'заявки']")

    # таблица "заявки"
    TABLE_APPS_HEADER = (By.CSS_SELECTOR, ".apps > .table__table-title")

    TABLE_APPS_TITLE_ID = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'ID']")
    TABLE_APPS_TITLE_DATE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Дата']")
    TABLE_APPS_TITLE_URGENCY = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Срочность']")
    TABLE_APPS_TITLE_STATUS = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Статус']")
    TABLE_APPS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Тип']")
    TABLE_APPS_TITLE_CAR = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Авто']")
    TABLE_APPS_TITLE_DESCRIPTION = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Описание']")



class HeaderLocators:

    # ИДЕНИТИФИКАЦИЯ СТР.       - <PAGE>_PAGE_NAME
    PAGE_ERROR_404 = (By.XPATH, "//*[contains(@id,'summary')]//span[text() = '(404)']")

    # КНОПКА ССЫЛКИ             - LINK_BTN_<NAME>
    LINK_BTN_CARS = (By.CSS_SELECTOR, "[href='/cars/']")
    LINK_BTN_DRIVERS = (By.CSS_SELECTOR, "[href='/drivers/']")
    LINK_BTN_DOCS = (By.CSS_SELECTOR, "[href='/documents/']")
    LINK_BTN_CARDS = (By.CSS_SELECTOR, "[href='/cards/']")
    LINK_BTN_APPS = (By.CSS_SELECTOR, "[href='/applications/']")
    LINK_BTN_ACCOUNT = (By.CSS_SELECTOR, "[href='/account/']")
    LINK_BTN_LOGOUT = (By.CSS_SELECTOR, ".auth__exit")

class LoginPageLocators:

    # ссылки
    # КНОПКА ССЫЛКИ             - LINK_BTN_<NAME>
    LINK_BTN_REG = (By.CSS_SELECTOR, "[href='/registration/']")
    LINK_BTN_ACC_ACTIVATION = (By.CSS_SELECTOR, "[href='/reg-activation/']")
    LINK_BTN_PASSWORD_CHANGE = (By.CSS_SELECTOR, "[href='/password-change/']")

    # Форма "авторизации"
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>

    FORM_LOGIN_TITLE = (By.CSS_SELECTOR, ".main__form")
    FORM_LOGIN_INPUT_EMAIL = (By.CSS_SELECTOR, "[id='id_username']")
    FORM_LOGIN_INPUT_PASSWORD = (By.CSS_SELECTOR, "[id='id_password']")
    FORM_LOGIN_BTN_SUBMIT = (By.CSS_SELECTOR, "[class='main__button']")

    # Ошибки FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_LOGIN_ERROR_LOGIN = (By.CSS_SELECTOR, ".errorlist.nonfield > li")

class RegistrationPageLocators:

    # Ссылки
    # КНОПКА ССЫЛКИ             - LINK_BTN_<NAME>
    LINK_BTN_LOGIN = (By.CSS_SELECTOR, "[href='/']")

    # Форма "регистрации"
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>

    FORM_REG_INPUT_EMAIL = (By.ID, "id_email")
    FORM_REG_INPUT_PASS1 = (By.ID, "id_password")
    FORM_REG_INPUT_PASS2 = (By.ID, "id_password_repeat")
    FORM_REG_INPUT_PHONE = (By.ID, "id_phone")
    FORM_REG_INPUT_F_NAME = (By.ID, "id_first_name")
    FORM_REG_INPUT_L_NAME = (By.ID, "id_last_name")
    FORM_REG_INPUT_P_NAME = (By.ID, "id_patronymic")
    # FORM_REG_SELECT_ROLE = (By.ID, "id_role")
    FORM_REG_BTN_SUBMIT = (By.CSS_SELECTOR, ".main__button")

    FORM_REG_ERROR_EMAIL = (By.XPATH, "//*[contains(@class,'errors')]//span[text() = 'Ваша почта не указана в списке "
                             "допустимых. Обратитесь к администратору']")
    FORM_REG_ERROR_PASS = (By.XPATH, "//*[contains(@class,'errors')]//span[text() = 'Пароли не совпадают!']")
    FORM_REG_ERROR_PHONE = (By.XPATH, "//*[contains(@class,'errors')]//span[text() = 'Номер телефона состоит из 11 цифр']")
    FORM_REG_ERROR_F_NAME = (By.XPATH, "//*[contains(@class,'errors')]//span[text() = 'имя может состоять только из Кириллицы!']")
    FORM_REG_ERROR_L_NAME = (By.XPATH, "//*[contains(@class,'errors')]//span[text() = 'фамилия может состоять только из Кириллицы!']")
    FORM_REG_ERROR_P_NAME = (By.XPATH, "//*[contains(@class,'errors')]//span[text() = 'отчество может состоять только из Кириллицы!']")

class ActivationPageLocators:

    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>

    FORM_ACTIVATION_INPUT_CODE = (By.ID, "id_activation_code")
    FORM_ACTIVATION_BTN_SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

class AccountPageLocators:

    # Форма редактирования "личных данных"
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>

    FORM_PERSONAL_INPUT_F_NAME = (By.ID, "id_first_name")
    FORM_PERSONAL_INPUT_L_NAME = (By.ID, "id_last_name")
    FORM_PERSONAL_INPUT_P_NAME = (By.ID, "id_patronymic")
    FORM_PERSONAL_INPUT_PHONE = (By.ID, "id_phone")
    FORM_PERSONAL_1INPUT_EMAIL = (By.ID, "id_email")
    FORM_PERSONAL_BTN_SUBMIT = (By.CSS_SELECTOR, ".account-area__btn-submit")


    # Сообщение о смене данных
    # MESSAGE:
    #           TEXT            - FORM_<FORM_NAME>_MSG_<MSG_NAME>_TEXT
    #           CROSS           - FORM_<FORM_NAME>_MSG_<MSG_NAME>_CROSS

    FORM_PERSONAL_MSG_SUCCESS_TEXT = (By.XPATH, "//*[contains(@class,'success')]//span[text() = 'Данные изменены!']")
    FORM_PERSONAL_MSG_SUCCESS_CROSS = (By.CSS_SELECTOR, "ul.messages > li.success > a.close")

    # Таблица "Автомобили"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_CARS_HEADER = (By.CSS_SELECTOR, ".cars > .table__table-title")

    TABLE_CARS_TITLE_REG_NUMBER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Номер']")
    TABLE_CARS_TITLE_BRAND = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Марка']")
    TABLE_CARS_TITLE_REGION_CODE = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Регион']")
    TABLE_CARS_TITLE_LAST_INSPECTION = (By.XPATH, "//*[contains(@class,'table__title')]//span[text() = 'Последний']")
    TABLE_CARS_TITLE_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'table__title')]//span[text() = 'заявки']")


    # Таблица "Топливные карты"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_CARDS_HEADER = (By.CSS_SELECTOR, ".cards > .table__table-title")

    TABLE_CARDS_TITLE_ID = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'ID']")
    TABLE_CARDS_TITLE_NUMBER = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Номер']")
    TABLE_CARDS_TITLE_LIMIT = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Лимит']")
    TABLE_CARDS_TITLE_BALANCE = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Остаток']")
    TABLE_CARDS_TITLE_ACTIONS = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Действия']")

    # Форма "изменение баланса карты"
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_CARD_BALANCE_INPUT_BALANCE = (By.CSS_SELECTOR, ".table__card-balance")
    FORM_CARD_BALANCE_BTN_SUBMIT = (By.CSS_SELECTOR, ".table__btn-save-balance")
    # MESSAGE:
    #           TEXT            - FORM_<FORM_NAME>_MSG_<MSG_NAME>_TEXT
    #           CROSS           - FORM_<FORM_NAME>_MSG_<MSG_NAME>_CROSS
    FORM_CARD_BALANCE_MSG_SUCCESS_TEXT = (By.XPATH, "//*[contains(@class,'success')]//span[text() = 'Баланс изменен!']")
    FORM_CARD_BALANCE_MSG_SUCCESS_CROSS = (By.CSS_SELECTOR, "ul.messages > li.success > a.close")

    # Таблица "Документы"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_DOCS_HEADER = (By.CSS_SELECTOR, ".docs > .table__table-title")

    TABLE_DOCS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'docs')]//th[text() = 'Тип документа']")
    TABLE_DOCS_TITLE_START_DATE = (By.XPATH, "//*[contains(@class,'docs')]//th[text() = 'Дата получения']")
    TABLE_DOCS_TITLE_END_DATE = (By.XPATH, "//*[contains(@class,'docs')]//th[text() = 'Дата окончания']")
    TABLE_DOCS_TITLE_COPY = (By.XPATH, "//*[contains(@class,'docs')]//th[text() = 'Копия файла']")
    TABLE_DOCS_TITLE_ACTIONS = (By.XPATH, "//*[contains(@class,'docs')]//th[text() = 'Удалить?']")

    # Форма "удаления документа"
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>

    FORM_DOC_DELETE_TITLE = (By.CSS_SELECTOR, ".confirm-delete")
    FORM_DOC_DELETE_BTN_OPEN = (By.CSS_SELECTOR, ".table__btn-delete-app[id*='doc-']")
    FORM_DOC_DELETE_BTN_SUBMIT = (By.ID, "btn-confirm-delete")
    FORM_DOC_DELETE_RESET = (By.ID, "btn-refuse-delete")

    # MESSAGE:
    #           TEXT            - FORM_<FORM_NAME>_MSG_<MSG_NAME>_TEXT
    #           CROSS           - FORM_<FORM_NAME>_MSG_<MSG_NAME>_CROSS
    FORM_DOC_DELETE_MSG_SUCCESS_TITLE = (By.XPATH, "//*[contains(@class,'success')]//span[text() = 'Документ успешно удален!']")
    FORM_DOC_DELETE_MSG_SUCCESS_CROSS = (By.CSS_SELECTOR, "ul.messages > li.success > a.close")

    # Форма добавления документов
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_DOC_ADD_TITLE = (By.CSS_SELECTOR, ".form-doc.add")

    FORM_DOC_ADD_BTN_OPEN = (By.CSS_SELECTOR, ".table__btn-add-doc")
    FORM_DOC_ADD_RADIO_TYPE = (By.CSS_SELECTOR, "label[for='id_type_0']")

    FORM_DOC_ADD_INPUT_START_DATE = (By.ID, "id_start_date")

    FORM_DOC_ADD_INPUT_END_DATE = (By.ID, "id_end_date")

    FORM_DOC_ADD_INPUT_COPY = (By.ID, "id_file")

    FORM_DOC_ADD_BTN_SUBMIT = (By.CSS_SELECTOR, ".form-app__timing button[type='submit']")
    FORM_DOC_ADD_RESET = (By.CSS_SELECTOR, ".bnt-form-doc-reset-add > svg")

    FORM_DOC_ADD_ERROR_DATE = (By.CSS_SELECTOR, ".form-app__timing > span > ul.errorlist")
    # MESSAGE:
    #           TEXT            - FORM_<FORM_NAME>_MSG_<MSG_NAME>_TEXT
    #           CROSS           - FORM_<FORM_NAME>_MSG_<MSG_NAME>_CROSS
    FORM_ADD_DOC_MSG_SUCCESS_TEXT = (By.XPATH, "//*[contains(@class,'success')]//span[text() = 'Документ добавлен!']")
    FORM_ADD_DOC_MSG_SUCCESS_CROSS = (By.CSS_SELECTOR, "ul.messages > li.success > a.close")

class CarsPageLocators:

    # Кол-во "автомобилей"
    INFO_CAR_COUNT_TITLE = (By.CSS_SELECTOR, ".main__title > h1")
    INFO_CAR_COUNT = (By.CSS_SELECTOR, ".main__title > p")
    INFO_NOT_CAR = (By.XPATH, "//*[contains(@class,'main__information')]//p[text() = 'Не найдено ']")
    # Форма добавления "автомобиля"
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_CAR_ADD_TITLE = (By.CSS_SELECTOR, ".form-car.add")
    FORM_CAR_ADD_BTN_OPEN = (By.CSS_SELECTOR, ".main__btn-add-car")
    FORM_CAR_ADD_INPUT_REG_NUMBER = (By.ID, "id_registration_number")
    FORM_CAR_ADD_SELECT_BRAND =(By.ID, "id_brand")
    FORM_CAR_ADD_INPUT_REGION = (By.ID, "id_region_code")
    FORM_CAR_ADD_INPUT_LAST_INSPECTION = (By.ID, "id_last_inspection")
    FORM_CAR_ADD_SELECT_DRIVER = (By.ID, "id_owner")

    FORM_CAR_ADD_BTN_SUBMIT = (By.CSS_SELECTOR, ".form-car.add  button[type='submit']")
    FORM_CAR_ADD_BTN_RESET = (By.CSS_SELECTOR, ".bnt-form-car-reset-add > svg")

    FORM_ADD_CAR_MSG_SUCCESS_TEXT = (By.XPATH, "//*[contains(@class,'success')]//span[text() = 'Машина добавлена']")
    FORM_ADD_CAR_MSG_SUCCESS_CROSS = (By.CSS_SELECTOR, "ul.messages > li.success > a.close")

    # Блок условий фильтрации
    # FILTERS:
    #       УСЛОВИЕ             - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<TITLE>
    #       ВАРИАНТ_УСЛОВИЕ     - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<CONDITION>
    #       КНОПКА УСЛОВИЯ      - FILTER_<FILTER_NAME>_BTN_SUBMIT
    #       СБРОС УСЛОВИЙ       - FILTER_<FILTER_NAME>_BTN_RESET

    FILTER_CARS_REG_NUMBER_TITLE = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='registration_number']")
    FILTER_CARS_REG_NUMBER_INPUT = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='registration_number']")

    FILTER_CARS_BRANDS_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Марка']")
    FILTER_CARS_BRANDS_CHECKS = (By.CSS_SELECTOR, "input[type='checkbox'][name='brand']")

    FILTER_CARS_HAS_DRIVER_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Водитель']")
    FILTER_CARS_HAS_DRIVER_CHECKS = (By.CSS_SELECTOR, "[id*='driver_']")
    # FILTER_CARS_DRIVERS_CHECK_0 = (By.ID, "driver_no")

    FILTER_CARS_REGIONS_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Регион']")
    FILTER_CARS_REGIONS_CHECKS = (By.CSS_SELECTOR, "input[type='checkbox'][name='region_code']")

    FILTER_CARS_APP_TYPES_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип заявки']")
    FILTER_CARS_APP_TYPES_CHECKS = (By.CSS_SELECTOR, "input[type='checkbox'][name='applications']")

    FILTER_CARS_BTN_SUBMIT = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_CARS_BTN_RESET = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "автомобили"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>

    TABLE_CARS_TITLE_REG_NUMBER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Номер']")
    TABLE_CARS_TITLE_DRIVER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Водитель']")
    TABLE_CARS_TITLE_BRAND = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Марка']")
    TABLE_CARS_TITLE_REGION_CODE = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Регион']")
    TABLE_CARS_TITLE_LAST_INSPECTION = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Последний осмотр']")
    TABLE_CARS_TITLE_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Активные заявки']")

    TABLE_CARS_TITLE_WITHDRAW = (By.XPATH, "//*[contains(@class,'cars')]//button[text() = 'Изъять']")
    TABLE_CARS_TITLE_DELETE = (By.XPATH, "//*[contains(@class,'cars')]//button[text() = 'Удалить']")

class DriversPageLocators:

    # Кол-во "водителей"
    INFO_DRIVER_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    INFO_DRIVER_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Блок условий фильтрации
    # FILTERS:
    #       УСЛОВИЕ             - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<TITLE>
    #       ВАРИАНТ_УСЛОВИЕ     - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<CONDITION>
    #       КНОПКА УСЛОВИЯ      - FILTER_<FILTER_NAME>_BTN_SUBMIT
    #       СБРОС УСЛОВИЙ       - FILTER_<FILTER_NAME>_BTN_RESET

    FILTER_DRIVERS_FIO_TITLE = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='last_name']")
    FILTER_DRIVERS_FIO_INPUT = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='last_name']")

    FILTER_DRIVERS_PHONE_TITLE = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='phone']")
    FILTER_DRIVERS_PHONE_INPUT = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='phone']")

    FILTER_APP_TYPE_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип заявки']")
    FILTER_DRIVERS_APPS_TYPE_CHECKS = (By.CSS_SELECTOR, "input[type='checkbox'][name='applications']")

    FILTER_CAR_BALANCE_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Карты']")
    FILTER_DRIVERS_CARD_BALANCE_RADIO_200 = (By.ID, "less_200")
    FILTER_DRIVERS_CARD_BALANCE_RADIO_0 = (By.ID, "no_cards")
    FILTER_DRIVERS_CARD_BALANCE_RADIO_1 = (By.ID, "more_cards")

    FILTER_DRIVERS_BTN_SUBMIT = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_DRIVERS_BTN_RESET = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "Водители"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_DRIVERS_TITLE_ID = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'ID']")
    TABLE_DRIVERS_TITLE_FIO = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'ФИО']")
    TABLE_DRIVERS_TITLE_PHONE = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Номер телефона']")
    TABLE_DRIVERS_TITLE_CARS = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Записанные машины']")
    TABLE_DRIVERS_TITLE_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Активные заявки']")
    TABLE_DRIVERS_TITLE_LIMIT = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Остаток на карте']")
    TABLE_DRIVERS_TITLE_DOCS = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Прикрепленные документы']")

class DocumentsPageLocators:

    # Кол-во документов
    INFO_DOC_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    INFO_DOC_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Блок условий фильтрации
    # FILTERS:
    #       УСЛОВИЕ             - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<TITLE>
    #       ВАРИАНТ_УСЛОВИЕ     - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<CONDITION>
    #       КНОПКА УСЛОВИЯ      - FILTER_<FILTER_NAME>_BTN_SUBMIT
    #       СБРОС УСЛОВИЙ       - FILTER_<FILTER_NAME>_BTN_RESET

    FILTER_DOCS_START_DATE_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'получение:']")
    FILTER_DOCS_START_DATE_INPUT = (By.CSS_SELECTOR, ".filtr-items__item > input[name='start_date']")

    FILTER_DOCS_END_DATE_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'окончание:']")
    FILTER_DOCS_END_DATE_INPUT = (By.CSS_SELECTOR, ".filtr-items__item > input[name='end_date']")

    FILTER_DOCS_C_OR_D_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Авто/Водитель']")
    FILTER_DOCS_C_OR_D_CAR_DOC = (By.ID, "auto")
    FILTER_DOCS_C_OR_D_DRIVER_DOC = (By.ID, "man")

    FILTER_DOCS_CAR_TYPES_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип (Авто)']")
    FILTER_DOCS_CAR_TYPES_CHECKS = (By.CSS_SELECTOR, "ul.car-doc input[name='doc_type']")

    FILTER_DOCS_DRIVER_TYPES_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип (Водитель)']")
    FILTER_DOCS_DRIVER_TYPES_CHECKS = (By.CSS_SELECTOR, "ul.driver-doc input[name='doc_type']")

    FILTER_DOCS_BTN_SUBMIT = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_DOCS_BTN_RESET = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "документы"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_DOCS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Тип документа']")
    TABLE_DOCS_TITLE_START_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата получения']")
    TABLE_DOCS_TITLE_END_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата окончания']")
    TABLE_DOCS_TITLE_CAR_OR_DRIVER = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Авто/Водитель']")
    TABLE_DOCS_TITLE_OWNER = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Владелец']")

class CardsPageLocators:

    # Кол-во "топливных карт"
    INFO_CARD_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    INFO_CARD_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Форма добавления топливных карт
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_CARD_ADD_BTN_OPEN = (By.CSS_SELECTOR, ".main__btn-add-card")
    FORM_CARD_ADD_INPUT_LIMIT = (By.ID, "id_limit")
    FORM_CARD_ADD_INPUT_NUMBER = (By.ID, "id_number")
    FORM_CARD_ADD_SELECT_OWNER = (By.ID, "id_owner")

    FORM_CARD_ADD_BTN_SUBMIT = (By.CSS_SELECTOR, ".form-card__timing > button[type='submit']")
    FORM_CARD_ADD_BTN_RESET = (By.CSS_SELECTOR, ".bnt-form-card-reset-add > svg")

    # Блок условий фильтрации
    # FILTERS:
    #       УСЛОВИЕ             - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<TITLE>
    #       ВАРИАНТ_УСЛОВИЕ     - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<CONDITION>
    #       КНОПКА УСЛОВИЯ      - FILTER_<FILTER_NAME>_BTN_SUBMIT
    #       СБРОС УСЛОВИЙ       - FILTER_<FILTER_NAME>_BTN_RESET

    FILTER_CARDS_NUMBER_TITLE = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='number']")
    FILTER_CARDS_NUMBER_INPUT = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='number']")

    FILTER_CARDS_OWNERS_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Владелец']")
    FILTER_CARDS_OWNERS_CHECKS_YES = (By.ID, "yes")
    FILTER_CARDS_OWNERS_CHECKS_NO = (By.ID, "no")

    FILTER_CARDS_LIMIT_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'лимит:']")
    FILTER_CARDS_LIMIT_INPUT_MIN = (By.CSS_SELECTOR, ".filtr-items__item > input[name='limit_min']")
    FILTER_CARDS_LIMIT_INPUT_MAX = (By.CSS_SELECTOR, ".filtr-items__item > input[name='limit_max']")

    FILTER_CARDS_BALANCE_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'остаток:']")
    FILTER_CARDS_BALANCE_INPUT_MIN = (By.CSS_SELECTOR, ".filtr-items__item > input[name='balance_min']")
    FILTER_CARDS_BALANCE_INPUT_MAX = (By.CSS_SELECTOR, ".filtr-items__item > input[name='balance_max']")

    FILTER_CARDS_BTN_SUBMIT = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_CARDS_BTN_RESET = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "топливные карты"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_CARDS_TITLE_ID = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'ID']")
    TABLE_CARDS_TITLE_NUMBER = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Номер']")
    TABLE_CARDS_TITLE_LIMIT = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Лимит']")
    TABLE_CARDS_TITLE_BALANCE = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Остаток']")
    TABLE_CARDS_TITLE_OWNER = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Владелец']")

    TABLE_CARDS_TITLE_WITHDRAW = (By.XPATH, "//*[contains(@class,'cards')]//button[text() = 'Изъять']")
    TABLE_CARDS_TITLE_DELETE = (By.XPATH, "//*[contains(@class,'cards')]//button[text() = 'Удалить']")

class ApplicationsPageLocators:

    # Кол-во заявок
    INFO_APP_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    INFO_APP_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Блок условий фильтрации
    # FILTERS:
    #       УСЛОВИЕ             - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<TITLE>
    #       ВАРИАНТ_УСЛОВИЕ     - FILTER_<FILTER_NAME>_<CONDITION_NAME>_<CONDITION>
    #       КНОПКА УСЛОВИЯ      - FILTER_<FILTER_NAME>_BTN_SUBMIT
    #       СБРОС УСЛОВИЙ       - FILTER_<FILTER_NAME>_BTN_RESET
    FILTER_APPS_START_DATE_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'получение:']")
    FILTER_APPS_START_DATE_INPUT = (By.CSS_SELECTOR, ".filtr-items__item > input[name='start_date']")

    FILTER_APPS_END_DATE_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'окончание:']")
    FILTER_APPS_END_DATE_INPUT = (By.CSS_SELECTOR, ".filtr-items__item > input[name='end_date']")

    FILTER_APPS_URGENCY_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Срочность']")
    FILTER_APPS_URGENCY_CHECKS_N = (By.ID, "N")
    FILTER_APPS_URGENCY_CHECKS_U = (By.ID, "U")
    FILTER_APPS_URGENCY_CHECKS_S = (By.ID, "S")

    FILTER_APPS_STATUS_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Статус']")
    FILTER_APPS_STATUS_CHECKS_WAIT_MANGER = (By.ID, "O")
    FILTER_APPS_STATUS_CHECKS_WAIT_ENGINEER = (By.ID, "OE")
    FILTER_APPS_STATUS_CHECKS_REPAIR = (By.ID, "REP")
    FILTER_APPS_STATUS_CHECKS_DONE = (By.ID, "V")
    FILTER_APPS_STATUS_CHECKS_OVERDUE = (By.ID, "P")
    FILTER_APPS_STATUS_CHECKS_REJECTED = (By.ID, "T")


    FILTER_APPS_TYPES_TITLE = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип']")
    FILTER_APPS_TYPES_CHECKS = (By.CSS_SELECTOR, "input[type='checkbox'][name='types_of_apps']")

    FILTER_APPS_BTN_SUBMIT = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_APPS_BTN_RESET = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "заявки"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_APPS_TITLE_ID = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'ID']")
    TABLE_APPS_TITLE_START_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата создания']")
    TABLE_APPS_TITLE_END_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата окончания']")
    TABLE_APPS_TITLE_URGENCY = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Статус']")
    TABLE_APPS_TITLE_STATUS = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Срочность']")
    TABLE_APPS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Тип']")
    TABLE_APPS_TITLE_OWNER = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Создатель']")
    TABLE_APPS_TITLE_CAR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Авто']")
    TABLE_APPS_TITLE_DESCR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Краткое описание']")

class CarPageLocators:

    # Форма редактирования данных авто
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_CAR_CHANGE_INPUT_IMAGE = (By.ID, "id_image")
    FORM_CAR_CHANGE_SELECT_BRAND = (By.ID, "id_brand")
    FORM_CAR_CHANGE_INPUT_REG_NUMBER = (By.ID, "id_registration_number")
    FORM_CAR_CHANGE_INPUT_REGION_CODE = (By.ID, "id_region_code")
    FORM_CAR_CHANGE_INPUT_LAST_INSPECTION = (By.ID, "id_last_inspection")
    FORM_CAR_CHANGE_SELECT_DRIVER = (By.ID, "id_owner")
    FORM_CAR_CHANGE_BTN_SUBMIT = (By.CSS_SELECTOR, ".car-area__btn-submit")

    # Форма добавления заявки
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_APP_ADD_BTN_OPEN = (By.CSS_SELECTOR, ".table__btn-add-app")
    FORM_APP_ADD_SELECT_TYPE = (By.ID, "id_type")
    FORM_APP_ADD_RADIO_URGENCY0 = (By.ID, "id_urgency_0")
    FORM_APP_ADD_RADIO_URGENCY1 = (By.ID, "id_urgency_1")
    FORM_APP_ADD_RADIO_URGENCY2 = (By.ID, "id_urgency_2")
    FORM_APP_ADD_SELECT_ENGINEER = (By.ID, "id_engineer")
    FORM_APP_ADD_INPUT_DESCRIPTION = (By.ID, "id_description")

    FORM_APP_ADD_BTN_SUBMIT = (By.CSS_SELECTOR, ".form-app.add.data-show-or-hide-form button[type='submit']")
    FORM_APP_ADD_BTN_RESET = (By.CSS_SELECTOR, ".bnt-form-app-reset-add > svg")

    # Таблица "Заявки"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_APPS_HEADER = (By.CSS_SELECTOR, "")
    TABLE_APPS_TITLE_ID = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'ID']")
    TABLE_APPS_TITLE_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата']")
    TABLE_APPS_TITLE_URGENCY = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Статус']")
    TABLE_APPS_TITLE_STATUS = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Срочность']")
    TABLE_APPS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Тип']")
    TABLE_APPS_TITLE_DESCR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Краткое описание']")

    # Форма добавления документа
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_DOC_ADD_BTN_OPEN = (By.CSS_SELECTOR, ".table__btn-add-doc")
    FORM_DOC_ADD_RADIO_TYPE = (By.CSS_SELECTOR, "[id*='id_type_']")

    FORM_DOC_ADD_INPUT_START_DATE = (By.ID, "id_start_date")

    FORM_DOC_ADD_INPUT_END_DATE = (By.ID, "id_end_date")

    FORM_DOC_ADD_INPUT_COPY = (By.ID, "id_file")

    FORM_DOC_ADD_BTN_SUBMIT = (By.CSS_SELECTOR, ".form-app__timing button[type='submit']")
    FORM_DOC_ADD_BTN_RESET = (By.CSS_SELECTOR, ".bnt-form-doc-reset-add > svg")

    # Таблица "Документы"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_DOCS_HEADER = (By.CSS_SELECTOR, ".docs > .table__table-title")

    TABLE_DOCS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Тип документа']")
    TABLE_DOCS_TITLE_START_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата получения']")
    TABLE_DOCS_TITLE_END_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата окончания']")
    TABLE_DOCS_TITLE_COPY = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Копия файла']")
    TABLE_DOCS_TITLE_ACTIONS = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Удалить?']")


class DriverPageLocators:

    # Информация о водителе
    INFO_DRIVER_FIRST_NAME = (By.ID, "id_first_name")
    INFO_DRIVER_LAST_NAME = (By.ID, "id_last_name")
    INFO_DRIVER_PATRONYMIC = (By.ID, "id_patronymic")
    INFO_DRIVER_PHONE = (By.ID, "id_phone")
    INFO_DRIVER_EMAIL = (By.ID, "id_email")

    # Таблица "Автомобили"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_CARS_HEADER = (By.CSS_SELECTOR, ".cars > .table__table-title")

    TABLE_CARS_TITLE_REG_NUMBER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Номер']")
    TABLE_CARS_TITLE_BRAND = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Марка']")
    TABLE_CARS_TITLE_REGION_CODE = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Регион']")
    TABLE_CARS_TITLE_LAST_INSPECTION = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Последний осмотр']")
    TABLE_CARS_TITLE_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Активные заявки']")

    # Таблица "Заявки"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_APPS_HEADER = (By.CSS_SELECTOR, ".applications > .table__table-title")

    TABLE_APPS_TITLE_ID = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'ID']")
    TABLE_APPS_TITLE_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата']")
    TABLE_APPS_TITLE_URGENCY = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Статус']")
    TABLE_APPS_TITLE_STATUS = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Срочность']")
    TABLE_APPS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Тип']")
    TABLE_APPS_TITLE_DESCR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Краткое описание']")

    # Таблица "Топливные карты"
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>
    TABLE_CARDS_HEADER = (By.CSS_SELECTOR, ".cards > .table__table-title")

    TABLE_CARDS_TITLE_ID = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'ID']")
    TABLE_CARDS_TITLE_NUMBER = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Номер']")
    TABLE_CARDS_TITLE_LIMIT = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Лимит']")
    TABLE_CARDS_TITLE_BALANCE = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Остаток']")
    TABLE_CARDS_TITLE_OWNER = ()

    # Форма присвоения "топливной карты"
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_CARD_ASSIGN_SELECT_NUMBER = ()
    FORM_CARD_ASSIGN_BTN_SUBMIT = ()
    FORM_CARD_ASSIGN_BTN_RESET = ()

    # Таблица "Документы
    # TABLE:
    #       HEADER              - TABLE_<TABLE_NAME>_HEADER
    #       TITLE               - TABLE_<TABLE_NAME>_TITLE_<TITLE_NAME>

    TABLE_DOCS_HEADER = (By.CSS_SELECTOR, ".docs > .table__table-title")

    TABLE_DOCS_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Тип документа']")
    TABLE_DOCS_TITLE_START_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата получения']")
    TABLE_DOCS_TITLE_END_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата окончания']")
    TABLE_DOCS_TITLE_COPY = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Копия файла']")
    TABLE_DOCS_TITLE_ACTIONS = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Удалить?']")

class AppPageLocators:

    # Информация о "заявке"
    INFO_APP_ID = (By.ID, "id_pk")
    INFO_APP_URGENCY =(By.ID, "id_urgency")
    INFO_APP_STATUS = (By.ID, "id_status")
    INFO_APP_START_DATE = (By.ID, "id_start_date")
    INFO_APP_CONSIDERATION = (By.ID, "id_consideration_date")
    INFO_APP_END_DATE = (By.ID, "id_end_date")
    INFO_APP_CREATOR = (By.ID, "id_creator")
    INFO_APP_ENGINEER = (By.ID, "id_engineer")
    INFO_APP_CAR = (By.ID, "id_car")

    # Форма изменения заявки
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_APP_CHANGE_BTN_OPEN = (By.CSS_SELECTOR, "info-app__btn-submit")

    FORM_APP_CHANGE_SELECT_TYPE = (By.ID, "id_type")
    FORM_APP_CHANGE_RADIO_URGENCY0 = (By.ID, "id_urgency_0")
    FORM_APP_CHANGE_RADIO_URGENCY1 = (By.ID, "id_urgency_1")
    FORM_APP_CHANGE_RADIO_URGENCY2 = (By.ID, "id_urgency_2")
    FORM_APP_CHANGE_SELECT_ENGINEER = (By.ID, "id_engineer")
    FORM_APP_CHANGE_INPUT_DESCRIPTION = (By.ID, "id_description")

    FORM_APP_CHANGE_BTN_SUBMIT = (By.CSS_SELECTOR, ".form-app.change.data-show-or-hide-form  button[type='submit']")
    FORM_APP_CHANGE_BTN_RESET = (By.CSS_SELECTOR, ".form-app.change.data-show-or-hide-form svg")

    # Форма удаления заявки
    # FORM:
    #       ОБЪЕКТ ФОРМЫ        - FORM_<FORM_NAME>_TITLE
    #       КНОПКА ОТКРЫТИЯ     - FORM_<FORM_NAME>_BTN_OPEN
    #       INPUT               - FORM_<FORM_NAME>_INPUT_<INPUT_NAME>
    #       RADIO               - FORM_<FORM_NAME>_RADIO_<RADIO_NAME>
    #       SELECT              - FORM_<FORM_NAME>_SELECT_<SELECT_NAME>
    #       SUBMIT BTN          - FORM_<FORM_NAME>FORM_APP_ADD_BTN_SUBMIT
    #       RESET BTN           - FORM_<FORM_NAME>_BTN_RESET
    #       ERROR               - FORM_<FORM_NAME>_ERROR_<ERROR_NAME>
    FORM_APP_DELETE_BTN_OPEN = (By.CSS_SELECTOR, "info-app__btn-delete")

    FORM_APP_DELETE_BTN_SUBMIT = (By.CSS_SELECTOR, ".confirm-delete.data-show-or-hide-form button[type='submit']")
    FORM_APP_DELETE_BTN_RESET = (By.CSS_SELECTOR, ".confirm-delete.data-show-or-hide-form button[id='notsubmit']")

    # Форма подтверждения заявки
    FORM_APP_CONFIRM_BTN_OPEN = (By.CSS_SELECTOR, "info-app__btn-confirm")

    FORM_APP_CONFIRM_INPUT_MANAGER_DESCR = (By.ID, "id_manager_descr")
    FORM_APP_CONFIRM_SELECT_ENGINEER = (By.CSS_SELECTOR, ".form-app.confirm.data-show-or-hide-form select[id='id_engineer']")

    # Форма возвращения заявки на доработку
    FORM_APP_REFUSE_BTN_OPEN = (By.CSS_SELECTOR, "info-app__btn-refuse")

    FORM_APP_REFUSE_BTN_SUBMIT = (By.CSS_SELECTOR, "confirm-refuse.data-show-or-hide-form button[type='submit']")
    FORM_APP_REFUSE_BTN_RESET = (By.CSS_SELECTOR, "confirm-refuse.data-show-or-hide-form button[id=notsubmit-refuse']")

