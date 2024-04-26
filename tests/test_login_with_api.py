import json

import allure
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have

from tests.conftest import get_cookie, URL

payload = {
    "product_attribute_72_5_18": '53',
    "product_attribute_72_6_19": '54',
    "product_attribute_72_3_20": '57',
    "addtocart_72.EnteredQuantity": '1'
}


def request_api_post(url, **kwargs):
    with step("API Request"):
        result = requests.post(url, **kwargs)
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True),
                      name="Response", attachment_type=AttachmentType.JSON, extension="json")
    return result


def test_add_to_cart_though_api():
    with step("Set cookie from API"):
        cookie = get_cookie()
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with step('Add to cart'):
        url = URL + '/addproducttocart/details/72/1'
        result = request_api_post(
            url,
            cookies={'NOPCOMMERCE.AUTH': cookie},
            data=payload
        )
        assert result.status_code == 200
    with step('Go to cart'):
        browser.element('.cart-label').click()

    with step('Check product details'):
        browser.element('.product-name').should(have.text('Build your own cheap computer'))
        browser.element('td.product').should(have.text('Processor: Medium [+15.00]'))
        browser.element('td.product').should(have.text('RAM: 2 GB'))
        browser.element('td.product').should(have.text('HDD: 320 GB'))

    with step("Clear cart with UI"):
        browser.element(".qty-input").clear()
        browser.element(".qty-input").set_value("0").press_enter()


def test_add_cell_phone_to_cart():
    cookie = get_cookie()

    browser.open('')
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
    browser.open('')

    with step("Add notebook to cart with API"):
        url = URL + "/addproducttocart/catalog/43/1/1"
        result = request_api_post(url, cookies={'NOPCOMMERCE.AUTH': cookie})

        assert result.json()["success"] is True

    with step("Check product detail"):
        browser.open("/cart")
        browser.element('.product-name').should(have.text("Smartphone"))

    with step("Clear cart with UI"):
        browser.element(".qty-input").clear()
        browser.element(".qty-input").set_value("0").press_enter()
