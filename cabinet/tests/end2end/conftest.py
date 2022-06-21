# Обработка командной строки.
# Указываем тип браузера.
# Указываем язык браузера с помощью WebDriver.
import time

import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from cabinet.models import MyUser


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                    help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en', help="Choose language")


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    browser = None
    if browser_name == "chrome":
        print("\nStart chome browser for test...")
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        print("\nStart firefox browser for test...")
        fp = webdriver.FirefoxProfile()
        fp.set_preference('intl.accept_languages', user_language)
        browser = webdriver.Firefox(firefox_profile=fp)
    else:
        # raise pytest.UsageError("--browser_name should be chrome or firefox")
        fp = webdriver.FirefoxProfile()
        fp.set_preference('intl.accept_languages', user_language)
        browser = webdriver.Firefox(firefox_profile=fp)
    yield browser
    print("\nClose browser...")
    time.sleep(3)
    browser.quit()

@pytest.fixture
def create_manager(db):
    password = "12345"
    MyUser.objects.create_user(
        email="test_manager@mail.com",
        password=password,
        first_name="Иван",
        last_name="Иванов",
        patronymic="Иванович",
        chat_id=1234,
        role='m',
        is_active=True,
    )

    my_user = MyUser.objects.first()
    print(f"{my_user=}")

    return MyUser.objects.first(), password