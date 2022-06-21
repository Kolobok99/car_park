from selenium.webdriver.common.by import By


class LoginPageLocators():
    # REG_LINK = (By.CSS_SELECTOR, "#login_link")
    # LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")
    # BASKET_LINK = (By.CSS_SELECTOR, "div.basket-mini.pull-right.hidden-xs > span > a")
    # BASKET_LINK_INVALID = (By.CSS_SELECTOR, "#basket_link_inc")
    # USER_ICON = (By.CSS_SELECTOR, ".icon-user")

    REG_LINK = (By.CSS_SELECTOR, "[href='/registration/']")
    ACC_ACTIVATION_LINK = (By.CSS_SELECTOR, "[href='/reg-activation/']")
    PASSWORD_CHANGE_LINK = (By.CSS_SELECTOR, "[href='/password-change/']")

    EMAIL_INPUT = (By.CSS_SELECTOR, "[id='id_username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[id='id_password']")
    BTN_SUBMIT = (By.CSS_SELECTOR, "[class='main__button']")
