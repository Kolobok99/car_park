from selenium.webdriver.common.by import By

class HeaderLocators:

    CARS_LINK = (By.CSS_SELECTOR, "[href='/cars/']")
    DRIVERS_LINK = (By.CSS_SELECTOR, "[href='/drivers/']")
    DOCS_LINK = (By.CSS_SELECTOR, "[href='/documents/']")
    CARDS_LINK = (By.CSS_SELECTOR, "[href='/cards/']")
    APPS_LINK = (By.CSS_SELECTOR, "[href='/applications/']")
    ACCOUNT_LINK = (By.CSS_SELECTOR, "[href='/account/']")

    LOGOUT_BTN = (By.CSS_SELECTOR, ".auth__exit")

class LoginPageLocators:

    # ссылки
    REG_LINK = (By.CSS_SELECTOR, "[href='/registration/']")
    ACC_ACTIVATION_LINK = (By.CSS_SELECTOR, "[href='/reg-activation/']")
    PASSWORD_CHANGE_LINK = (By.CSS_SELECTOR, "[href='/password-change/']")

    # Форма "авторизации"
    EMAIL_INPUT = (By.CSS_SELECTOR, "[id='id_username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[id='id_password']")
    BTN_SUBMIT = (By.CSS_SELECTOR, "[class='main__button']")

    # Ошибки
    LOGIN_ERROR = (By.CSS_SELECTOR, ".errorlist.nonfield > li")


class RegistrationPageLocators:

    # Ссылки
    LOGIN_LINK = (By.CSS_SELECTOR, "[href='/']")

    # Форма "регистрации"
    EMAIL_INPUT = (By.ID, "id_email")
    PASS_INPUT = (By.ID, "id_password")
    PASS2_INPUT = (By.ID, "id_password_repeat")
    PHONE_INPUT = (By.ID, "id_phone")
    NAME_INPUT = (By.ID, "id_first_name")
    LAST_NAME_INPUT = (By.ID, "id_last_name")
    PATRONYMIC_INPUT = (By.ID, "id_patronymic")
    ROLE_SELECT = (By.ID, "id_role")

    SUBMIT_BTN = (By.CSS_SELECTOR, ".main__button")

class AccountPageLocators:

    # Форма редактирования "личных данных"
    NAME_INPUT = (By.ID, "id_first_name")
    LAST_NAME_INPUT = (By.ID, "id_last_name")
    PATRONYMIC_INPUT = (By.ID, "id_patronymic")
    PHONE_INPUT = (By.ID, "id_phone")
    EMAIL_INPUT = (By.ID, "id_email")
    CHANGE_BTN = (By.CSS_SELECTOR, "account-area__btn-submit")

    # Таблица "Автомобили"
    CAR_TITLE = (By.CSS_SELECTOR, ".cars > .table__table-title")

    TABLE_TITLE_CAR_REG_NUMBER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Номер']")
    TABLE_TITLE_CAR_BRAND = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Марка']")
    TABLE_TITLE_CAR_REGION_CODE = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Регион']")
    TABLE_TITLE_CAR_LAST_INSPECTION = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Последний осмотр']")
    TABLE_TITLE_CAR_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Активные заявки']")

    # Таблица "Заявки"
    APP_TITLE = (By.CSS_SELECTOR, ".apps > .table__table-title")

    TABLE_TITLE_APP_ID = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'ID']")
    TABLE_TITLE_APP_DATE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Дата']")
    TABLE_TITLE_APP_URGENCY = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Срочность']")
    TABLE_TITLE_APP_STATUS = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Статус']")
    TABLE_TITLE_APP_TYPE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Тип']")
    TABLE_TITLE_APP_CAR = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Авто']")
    TABLE_TITLE_APP_DESCRIPTION = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Краткое описание']")

    # Таблица "Топливные карты"
    CARD_TITLE = (By.CSS_SELECTOR, ".cards > .table__table-title")

    TABLE_TITLE_CARD_ID = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'ID']")
    TABLE_TITLE_CARD_NUMBER = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Номер']")
    TABLE_TITLE_CARD_LIMIT = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Лимит']")
    TABLE_TITLE_CARD_BALANCE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Остаток']")
    TABLE_TITLE_CARD_ACTIONS = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Действия']")

    # Таблица "Документы"
    DOC_TITLE = (By.CSS_SELECTOR, ".docs > .table__table-title")

    TABLE_TITLE_DOC_TYPE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Тип документа']")
    TABLE_TITLE_DOC_START_DATE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Дата получения']")
    TABLE_TITLE_DOC_END_DATE = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Дата окончания']")
    TABLE_TITLE_DOC_COPY = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Копия файла']")
    TABLE_TITLE_DOC_ACTIONS = (By.XPATH, "//*[contains(@class,'apps')]//th[text() = 'Удалить?']")

    # Форма добавления документов
    DOC_ADD_BTN = (By.CSS_SELECTOR, ".table__btn-add-doc")
    DOC_TYPE_RADIO = (By.CSS_SELECTOR, "[id*='id_type_']")

    START_DATE = (By.ID, "id_start_date")

    END_DATE = (By.ID, "id_end_date")

    DOC_COPY_BTN = (By.ID, "id_file")

    DOC_SUBMIT_BTN = (By.CSS_SELECTOR, ".form-app__timing button[type='submit']")
    CLOSE_DOC_FORM = (By.CSS_SELECTOR, ".bnt-form-doc-reset-add > svg")

class CarsPageLocators:

    # Кол-во "автомобилей"
    CAR_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    CAR_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Форма добавления "автомобиля"
    ADD_CAR_BTN = (By.CSS_SELECTOR, ".main__btn-add-car")
    REG_NUMBER_INPUT = (By.ID, "id_registration_number")
    BRAND_INPUT =(By.ID, "id_brand")
    REGION_INPUT = (By.ID, "id_region_code")
    LAST_INSPECTION_INPUT = (By.ID, "id_last_inspection")
    DRIVER_SELECT = (By.ID, "id_owner")

    SUBMIT_BTN = (By.ID, ".form-car.add.data-show-or-hide-form  button[type='submit']")
    RESET_BTN = (By.CSS_SELECTOR, ".bnt-form-car-reset-add > svg")

    # Блок условий фильтрации
    REG_NUMBER_TITLE_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='registration_number']")
    REG_NUMBER_INPUT_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='registration_number']")

    BRANDS_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Марка']")
    BRANDS_CHECKS_FILTER = (By.CSS_SELECTOR, "input[type='checkbox'][name='brand']")

    DRIVER_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Водитель']")
    DRIVER_YES_CHECK_FILTER = (By.CSS_SELECTOR, "input[type='checkbox'][name='driver_has']")
    DRIVER_NO_CHECK_FILTER = ()

    REGION_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Регион']")
    REGIONS_CHECKS_FILTER = (By.CSS_SELECTOR, "input[type='checkbox'][name='region']")

    APP_TYPES_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип заявки']")
    APP_TYPES_CHECKS_FILTER = (By.CSS_SELECTOR, "input[type='checkbox'][name='applications']")

    FILTER_SUBMIT_BTN = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_RESET_BTN = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "автомобили"
    TABLE_TITLE_REG_NUMBER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Номер']")
    TABLE_TITLE_DRIVER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Водитель']")
    TABLE_TITLE_BRAND = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Марка']")
    TABLE_TITLE_REGION_CODE = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Регион']")
    TABLE_TITLE_LAST_INSPECTION = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Последний осмотр']")
    TABLE_TITLE_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Активные заявки']")

    TABLE_TITLE_WITHDRAW = (By.XPATH, "//*[contains(@class,'cars')]//button[text() = 'Изъять']")
    TABLE_TITLE_DELETE = (By.XPATH, "//*[contains(@class,'cars')]//button[text() = 'Удалить']")

class DriversPageLocators:

    # Кол-во "водителей"
    DRIVER_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    DRIVER_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Блок условий фильтрации
    FIO_TITLE_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='last_name']")
    FIO_INPUT_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='last_name']")

    PHONE_TITLE_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='phone']")
    PHONE_INPUT_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='phone']")

    APP_TYPE_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип заявки']")
    APPS_TYPE_CHECKS_FILTER = (By.CSS_SELECTOR, "input[type='checkbox'][name='applications']")

    CAR_BALANCE_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Карты']")
    CARD_BALANCE_200 = (By.ID, "less_200")
    CARD_NOT = (By.ID, "no_cards")
    CARD_ENOUGH = (By.ID, "more_cards")

    FILTER_SUBMIT_BTN = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_RESET_BTN = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "Водители"
    TABLE_TITLE_ID = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'ID']")
    TABLE_TITLE_FIO = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'ФИО']")
    TABLE_TITLE_PHONE = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Номер телефона']")
    TABLE_TITLE_CARS = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Записанные машины']")
    TABLE_TITLE_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Активные заявки']")
    TABLE_TITLE_LIMIT = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Остаток на карте']")
    TABLE_TITLE_DOCS = (By.XPATH, "//*[contains(@class,'drivers')]//th[text() = 'Прикрепленные документы']")

class DocumentsPageLocators:

    # Кол-во документов
    DOC_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    DOC_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Блок условий фильтрации
    START_DATE_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'получение:']")
    START_DATE_INPUT_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='start_date']")

    END_DATE_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'окончание:']")
    END_DATE_INPUT_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='end_date']")

    CAR_DOC_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Авто/Водитель']")
    CAR_DOC_CHECK_FILTER = (By.ID, "auto")
    DRIVER_DOC_CHECK_FILTER = (By.ID, "man")

    CAR_TYPES_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип (Авто)']")
    CAR_TYPES_CHECKS_FILTER = (By.CSS_SELECTOR, "ul.car-doc input[name='doc_type']")

    DRIVER_TYPES_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип (Водитель)']")
    DRIVER_TYPES_CHECKS_FILTER = (By.CSS_SELECTOR, "ul.driver-doc input[name='doc_type']")

    FILTER_SUBMIT_BTN = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_RESET_BTN = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "документы"
    TABLE_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Тип документа']")
    TABLE_TITLE_START_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата получения']")
    TABLE_TITLE_END_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата окончания']")
    TABLE_TITLE_CAR_OR_DRIVER = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Авто/Водитель']")
    TABLE_TITLE_OWNER = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Владелец']")

class CardsPageLocators:

    # Кол-во "топливных карт"
    CARD_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    CARD_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Форма добавления топливных карт
    ADD_CARD_BTN = (By.CSS_SELECTOR, ".main__btn-add-card")
    LIMIT_INPUT = (By.ID, "id_limit")
    NUMBER_INPUT = (By.ID, "id_number")
    OWNER_SELECT = (By.ID, "id_owner")

    SUBMIT_BTN = (By.CSS_SELECTOR, ".form-card__timing > button[type='submit']")
    RESET_BTN = (By.CSS_SELECTOR, ".bnt-form-card-reset-add > svg")

    # Блок условий фильтрации
    NUMBER_INPUT_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='number']")
    NUMBER_TITLE_FILTER = (By.CSS_SELECTOR, ".main__filtration.filtr-items input[name='number']")

    OWNERS_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Владелец']")
    OWNERS_YES_FILTER = (By.ID, "yes")
    OWNERS_NO_FILTER = (By.ID, "no")

    LIMIT_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'лимит:']")
    LIMIT_INPUT_FROM_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='limit_min']")
    LIMIT_INPUT_BEFORE_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='limit_max']")

    BALANCE_TITLE_FROM_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'остаток:']")
    BALANCE_INPUT_FROM_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='balance_min']")
    BALANCE_INPUT_BEFORE_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='balance_max']")

    FILTER_SUBMIT_BTN = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_RESET_BTN = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "топливные карты"
    TABLE_TITLE_ID = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'ID']")
    TABLE_TITLE_NUMBER = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Номер']")
    TABLE_TITLE_LIMIT = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Лимит']")
    TABLE_TITLE_BALANCE = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Остаток']")
    TABLE_TITLE_OWNER = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Владелец']")

    TABLE_TITLE_WITHDRAW = (By.XPATH, "//*[contains(@class,'cards')]//button[text() = 'Изъять']")
    TABLE_TITLE_DELETE = (By.XPATH, "//*[contains(@class,'cards')]//button[text() = 'Удалить']")

class ApplicationsPageLocators:

    # Кол-во заявок
    APP_TITLE_COUNT = (By.CSS_SELECTOR, ".main__title > h1")
    APP_COUNT = (By.CSS_SELECTOR, ".main__title > p")

    # Блок условий фильтрации
    START_DATE_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'получение:']")
    START_DATE_INPUT_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='start_date']")

    END_DATE_TITLE_FILTER = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'окончание:']")
    END_DATE_DAY_INPUT_FILTER = (By.CSS_SELECTOR, ".filtr-items__item > input[name='end_date']")

    URGENCY_TITLE_FILTERS = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Срочность']")
    N_URGENCY_FILTERS = (By.ID, "N")
    U_URGENCY_FILTERS = (By.ID, "U")
    S_URGENCY_FILTERS = (By.ID, "S")

    STATUS_TITLE_FILTERS = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Статус']")
    WAIT_MANGER_STATUS_FILTERS = (By.ID, "O")
    WAIT_ENGINEER_STATUS_FILTERS = (By.ID, "OE")
    REPAIR_STATUS_FILTERS = (By.ID, "REP")
    DONE_STATUS_FILTERS = (By.ID, "V")
    OVERDUE_STATUS_FILTERS = (By.ID, "P")
    REJECTED_STATUS_FILTERS = (By.ID, "T")


    TYPES_TITLE_FILTERS = (By.XPATH, "//*[contains(@class,'filtr-items__item')]//p[text() = 'Тип']")
    TYPES_CHECKS_FILTERS = (By.CSS_SELECTOR, "input[type='checkbox'][name='types_of_apps']")

    FILTER_SUBMIT_BTN = (By.CSS_SELECTOR, "button.filtr-items__button")
    FILTER_RESET_BTN = (By.CSS_SELECTOR, ".btn-reset")

    # Таблица "заявки"
    TABLE_TITLE_ID = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'ID']")
    TABLE_TITLE_START_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата создания']")
    TABLE_TITLE_END_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата окончания']")
    TABLE_TITLE_URGENCY = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Статус']")
    TABLE_TITLE_STATUS = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Срочность']")
    TABLE_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Тип']")
    TABLE_TITLE_OWNER = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Создатель']")
    TABLE_TITLE_CAR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Авто']")
    TABLE_TITLE_DESCR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Краткое описание']")

class CarPageLocators:

    # Форма редактирования данных авто
    IMAGE_INPUT = (By.ID, "id_image")
    BRAND_SELECT = (By.ID, "id_brand")
    REG_NUMBER_INPUT = (By.ID, "id_registration_number")
    REGION_CODE_INPUT = (By.ID, "id_region_code")
    LAST_INSPECTION_INPUT = (By.ID, "id_last_inspection")
    DRIVER_SELECT = (By.ID, "id_owner")
    CHANGE_BTN = (By.CSS_SELECTOR, ".car-area__btn-submit")

    # Форма добавления заявки
    ADD_APP_BTN = (By.CSS_SELECTOR, ".table__btn-add-app")
    APP_TYPE_SELECT = (By.ID, "id_type")
    NOT_URGENCY_RADIO = (By.ID, "id_urgency_0")
    URGENCY_RADIO = (By.ID, "id_urgency_1")
    VERY_URGENCY_RADIO = (By.ID, "id_urgency_2")
    ENGINEER_SELECT = (By.ID, "id_engineer")
    APP_DESCRIPTION_INPUT = (By.ID, "id_description")

    APP_SUBMIT_BTN = (By.CSS_SELECTOR, ".form-app.add.data-show-or-hide-form button[type='submit']")
    CLOSE_APP_FORM = (By.CSS_SELECTOR, ".bnt-form-app-reset-add > svg")

    # Таблица "Заявки"
    APP_TITLE = (By.CSS_SELECTOR, "")
    TABLE_TITLE_ID = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'ID']")
    TABLE_TITLE_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата']")
    TABLE_TITLE_URGENCY = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Статус']")
    TABLE_TITLE_STATUS = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Срочность']")
    TABLE_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Тип']")
    TABLE_TITLE_DESCR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Краткое описание']")

    # Форма добавления документа
    DOC_ADD_BTN = (By.CSS_SELECTOR, ".table__btn-add-doc")
    DOC_TYPE_RADIO = (By.CSS_SELECTOR, "[id*='id_type_']")

    START_DATE = (By.ID, "id_start_date")

    END_DATE = (By.ID, "id_end_date")

    DOC_COPY_BTN = (By.ID, "id_file")

    DOC_SUBMIT_BTN = (By.CSS_SELECTOR, ".form-app__timing button[type='submit']")
    CLOSE_DOC_FORM = (By.CSS_SELECTOR, ".bnt-form-doc-reset-add > svg")

    # Таблица "Документы"
    DOC_TITLE = (By.CSS_SELECTOR, ".docs > .table__table-title")

    TABLE_TITLE_DOC_TYPE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Тип документа']")
    TABLE_TITLE_DOC_START_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата получения']")
    TABLE_TITLE_DOC_END_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата окончания']")
    TABLE_TITLE_DOC_COPY = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Копия файла']")
    TABLE_TITLE_DOC_ACTIONS = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Удалить?']")


class DriverPageLocators:

    # Информация о водителе
    FIRST_NAME = (By.ID, "id_first_name")
    LAST_NAME = (By.ID, "id_last_name")
    PATRONYMIC = (By.ID, "id_patronymic")
    PHONE = (By.ID, "id_phone")
    EMAIL = (By.ID, "id_email")

    # Таблица "Автомобили"
    CAR_TITLE = (By.CSS_SELECTOR, ".cars > .table__table-title")

    TABLE_TITLE_CAR_REG_NUMBER = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Номер']")
    TABLE_TITLE_CAR_BRAND = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Марка']")
    TABLE_TITLE_CAR_REGION_CODE = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Регион']")
    TABLE_TITLE_CAR_LAST_INSPECTION = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Последний осмотр']")
    TABLE_TITLE_CAR_ACTIVE_APPS = (By.XPATH, "//*[contains(@class,'cars')]//th[text() = 'Активные заявки']")

    # Таблица "Заявки"
    APP_TITLE = (By.CSS_SELECTOR, ".applications > .table__table-title")

    TABLE_TITLE_ID = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'ID']")
    TABLE_TITLE_DATE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Дата']")
    TABLE_TITLE_URGENCY = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Статус']")
    TABLE_TITLE_STATUS = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Срочность']")
    TABLE_TITLE_TYPE = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Тип']")
    TABLE_TITLE_DESCR = (By.XPATH, "//*[contains(@class,'applications')]//th[text() = 'Краткое описание']")

    # Таблица "Топливные карты"
    CARD_TITLE = (By.CSS_SELECTOR, ".cards > .table__table-title")

    TABLE_TITLE_CARD_ID = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'ID']")
    TABLE_TITLE_CARD_NUMBER = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Номер']")
    TABLE_TITLE_CARD_LIMIT = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Лимит']")
    TABLE_TITLE_CARD_BALANCE = (By.XPATH, "//*[contains(@class,'cards')]//th[text() = 'Остаток']")
    TABLE_TITLE_CARD_OWNER = ()

    # Форма присвоения "топливной карты"
    NUMBER_INPUT_SELECT = ()
    SUBMIT_BTN = ()
    RESET_BTN = ()

    # Таблица "Документы
    DOC_TITLE = (By.CSS_SELECTOR, ".docs > .table__table-title")

    TABLE_TITLE_DOC_TYPE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Тип документа']")
    TABLE_TITLE_DOC_START_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата получения']")
    TABLE_TITLE_DOC_END_DATE = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Дата окончания']")
    TABLE_TITLE_DOC_COPY = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Копия файла']")
    TABLE_TITLE_DOC_ACTIONS = (By.XPATH, "//*[contains(@class,'documents')]//th[text() = 'Удалить?']")

class AppPageLocators:

    # Информация о "заявке"
    ID = (By.ID, "id_pk")
    URGENCY =(By.ID, "id_urgency")
    STATUS = (By.ID, "id_status")
    START_DATE = (By.ID, "id_start_date")
    CONSIDERATION = (By.ID, "id_consideration_date")
    END_DATE = (By.ID, "id_end_date")
    CREATOR = (By.ID, "id_creator")
    ENGINEER = (By.ID, "id_engineer")
    CAR = (By.ID, "id_car")

    # Форма изменения заявки
    APP_CHANGE_BTN = (By.CSS_SELECTOR, "info-app__btn-submit")

    APP_TYPE_SELECT = (By.ID, "id_type")
    NOT_URGENCY_RADIO = (By.ID, "id_urgency_0")
    URGENCY_RADIO = (By.ID, "id_urgency_1")
    VERY_URGENCY_RADIO = (By.ID, "id_urgency_2")
    CHANGE_ENGINEER_SELECT = (By.ID, "id_engineer")
    APP_DESCRIPTION = (By.ID, "id_description")

    APP_SUBMIT_BTN = (By.CSS_SELECTOR, ".form-app.change.data-show-or-hide-form  button[type='submit']")
    CLOSE_APP_FORM = (By.CSS_SELECTOR, ".form-app.change.data-show-or-hide-form svg")

    # Форма удаления заявки
    APP_DELETE_BTN = (By.CSS_SELECTOR, "info-app__btn-delete")

    APP_DELETE_YES = (By.CSS_SELECTOR, ".confirm-delete.data-show-or-hide-form button[type='submit']")
    APP_DELETE_NO = (By.CSS_SELECTOR, ".confirm-delete.data-show-or-hide-form button[id='notsubmit']")

    # Форма подтверждения заявки
    APP_CONFIRM_BTN = (By.CSS_SELECTOR, "info-app__btn-confirm")

    MANAGER_DESCR_INPUT = (By.ID, "id_manager_descr")
    CONFIRM_ENGINEER_SELECT = (By.CSS_SELECTOR, ".form-app.confirm.data-show-or-hide-form select[id='id_engineer']")

    # Форма возвращения заявки на доработку
    APP_REFUSE_BTN = (By.CSS_SELECTOR, "info-app__btn-refuse")

    APP_RETURN_YES = (By.CSS_SELECTOR, "confirm-refuse.data-show-or-hide-form button[type='submit']")
    APP_RETURN_NO = (By.CSS_SELECTOR, "confirm-refuse.data-show-or-hide-form button[id=notsubmit-refuse']")

