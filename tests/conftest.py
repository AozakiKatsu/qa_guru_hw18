import allure
import pytest
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser

LOGIN = "ira@example.com"
PASSWORD = "123456"
URL = "https://demowebshop.tricentis.com/"


def get_cookie():
    with step("Login with API"):
        result = requests.post(
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    with step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    return cookie


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    browser.config.base_url = URL
    browser.config.window_width = '1920'
    browser.config.window_height = '1080'
    browser.config.timeout = 6
