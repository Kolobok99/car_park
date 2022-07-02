import pytest

from cabinet.models import MyUser, WhiteListEmail
from cabinet.tests.end2end.new_pages.new_acc_activat_page import AccountActivationPage
from cabinet.tests.end2end.new_pages.new_login_page import LoginPage

from cabinet.tests.end2end.new_pages.new_reg_page import RegistrationPage


LINK = "/registration/"
class TestRegistrationPage():

    def test_this_is_registration_page(self, browser, live_server):
        """Тест: это стр. регистрации?"""
        # Инициализации объекта "регистрация"
        page = RegistrationPage(browser, live_server.url + LINK)
        # Гость заходит на стр. "регистрация"
        page.open()

        # Гость проверяет, что он на стр. "регистрации"
        page.should_be_registration_page()

    def test_quest_should_see_login_link(self, browser, live_server):
        """Тест: наличие ссылки на стр. авторизации"""

        # Инициализации объекта "регистрация"
        page = RegistrationPage(browser, live_server.url + LINK)
        # Гость переходит на стр. "регистрация"
        page.open()

        # Гость нажимает на кнопку "Войти"
        page.go_to_login_page_by_href()
        # Инициализация объекта "Логин"
        login_page = LoginPage(browser, browser.current_url)
        # Гость проверяет, что он на стр. "/"
        login_page.should_be_login_page(live_server)

    def test_guest_should_see_registration_form(self, browser, live_server):
        """Тест: наличие формы регистрации"""

        # Инициализации объекта "регистрация"
        page = RegistrationPage(browser, live_server.url + LINK)
        # Гость переходит на стр. "регистрация"
        page.open()
        # Гость проверяет наличие формы регистрации
        page.should_be_registration_form()

    @pytest.mark.django_db
    def test_driver_can_sing_up_with_valid_data(self, browser, create_user, live_server):
        """Тест: возможность зарегистрироваться
        с валидными данными и войти в ЛК """
        # Инициализации объекта "регистрация"
        page = RegistrationPage(browser, live_server.url + LINK)
        # Гость переходит на стр. "регистрация"
        page.open()

        # Получаем форму регистрации
        form_data = page.should_be_registration_form()


        # Добавление email'а в список разрешенных
        email = 'new_test_driver@mail.ru'
        WhiteListEmail.objects.create(email=email)

        # Инициализация данных регистрации
        reg_data = {}
        reg_data['email'] = email
        reg_data['pass1'] = '12345'
        reg_data['pass2'] = '12345'
        reg_data['phone'] = '89220986754'
        reg_data['f_name'] = 'Иван'
        reg_data['l_name'] = 'Петров'
        reg_data['p_name'] = 'Александрович'

        # Гость вводит данные, нажимает кнопку "отправить"
        page.guest_sign_up_as_driver(reg_data, form_data)

        # Получение кода активации
        new_test_driver = MyUser.objects.get(email=email)
        activation_code = new_test_driver.activation_code

        # Водитель переходит на стр. 'активация'
        activation_page = AccountActivationPage(browser, browser.current_url)

        # Водитель проверяет, что он на стр. активации
        activation_page.should_be_activation_page()
        # Получаем данные формы активации
        form_data = activation_page.should_be_activation_form()
        # Водитель вводит код активации и нажимает кнопку "отправить"
        activation_page.user_activate_account(code=activation_code, form_data=form_data)

        # Переход на стр. "авторизации"
        login_page = LoginPage(browser, browser.current_url)
        # Водитель проверяет, что он на стр. "авторизации"
        login_page.should_be_login_page(live_server)
        # Получаем данные формы авторизации
        login_form = login_page.should_be_sign_in_form()
        # Водитель вводит учетные данные и нажимает кнопку "отправить"
        login_page.user_sign_in(email=email, password='12345', form_data=login_form)


    @pytest.mark.django_db
    def test_driver_canT_sing_up_with_INvalid_data(self, browser, create_user, live_server):
        """Тест: возможность зарегистрироваться
        с НЕвалидными данными"""
        # Инициализации объекта "регистрация"
        page = RegistrationPage(browser, live_server.url + LINK)
        # Гость переходит на стр. "регистрация"
        page.open()

        # Получаем форму регистрации
        form_data = page.should_be_registration_form()

        # Инициализация данных для регистрации
        reg_data = {}
        reg_data['email'] = 'not_white_mail@mail.ru'
        reg_data['pass1'] = '12345'
        reg_data['pass2'] = '543211231'
        reg_data['phone'] = '123456789a'
        reg_data['f_name'] = 'Ivan'
        reg_data['l_name'] = 'Петров123'
        reg_data['p_name'] = 'Alександрович'

        # Гость вводит данные, нажимает кнопку "отправить"
        page.guest_sign_up_as_driver(reg_data, form_data)
        # Гость видит сообщения об ошибках
        page.should_by_sign_up_errors()