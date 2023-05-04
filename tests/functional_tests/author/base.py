import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.browser import make_chrome_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form_by_xpath(self, xpath):
        return self.browser.find_element(
            By.XPATH,
            f'{xpath}'
        )

    def sleep(self, seconds=5):
        time.sleep(seconds)
