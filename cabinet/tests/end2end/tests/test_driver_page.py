import pytest

from cabinet.models import MyUser, CarBrand
from cabinet.tests.end2end.pages.account_page import AccountPage
from cabinet.tests.end2end.pages.reg_page import RegistrationPage
from cabinet.tests.end2end.pages.login_page import LoginPage

LINK = " "
class TestDriverPage:

    @pytest.mark.skip
    def test_this_is_driver_page(self, browser, live_server):
        pass