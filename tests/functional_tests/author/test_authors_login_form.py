import pytest

from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest
from accounts.models import User


@pytest.mark.functional_test
class AuthorsLoginFormTest(AuthorsBaseTest):
    def setUp(self):
        self.user = User.objects.create_user(
            email='dummy@gmail.com',
            password='P4ssW0rD'
        )

        return super().setUp()

    def setup_to_test_login_form(self, email_data, password_data, expected_message):
        url = reverse('accounts:login')

        # User opens our site
        self.browser.get(f'{self.live_server_url}{url}')

        # See the form and click on the email/password fields
        form = self.get_form_by_xpath(
            '/html/body/main/div[2]/form/div[1]'
        )
        email = self.get_by_placeholder(form, 'Type your e-mail')
        password = self.get_by_placeholder(form, 'Type your password')

        # User fill the email and password fields
        email.send_keys(email_data)
        password.send_keys(password_data)

        # And submit the form
        form.submit()

        self.assertIn(
            expected_message,
            self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_form_with_valid_data_login_successfully(self):
        self.setup_to_test_login_form(
            'dummy@gmail.com', 'P4ssW0rD', 'You have been login successfully, enjoy our site!')

    def test_login_form_with_empty_data(self):
        self.setup_to_test_login_form(
            '  ', '  ', '')

    def test_login_form_raises_error_when_credentials_are_wrong(self):
        self.setup_to_test_login_form(
            'dummy@gmail.com', 'P4ssW0rDe', 'Your e-mail or password are wrong. Fix them and try again',
        )
