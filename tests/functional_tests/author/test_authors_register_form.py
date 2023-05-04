import pytest

from django.urls import reverse
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from .base import AuthorsBaseTest
from accounts.forms import UserRegisterForm


@pytest.mark.functional_test
class AuthorsRegisterFormTest(AuthorsBaseTest):
    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'The e-mail gotta be valid'),
        ('password', 'The password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_empty_fields_error_message(self, field, error):
        url = reverse('accounts:register')

        self.browser.get(f'{self.live_server_url}{url}')

        register_form = UserRegisterForm()
        placeholder = register_form[field].field.widget.attrs['placeholder']

        page_form = self.get_form_by_xpath(
            '/html/body/main/div[2]/form/div[1]')

        self.fill_form_dummy_data(page_form)

        if field != 'email':
            page_form.find_element(
                By.NAME,
                'email'
            ).send_keys('dummy@email.com')
        else:
            page_form.find_element(
                By.NAME,
                'email'
            ).send_keys('dummy@invalid')

        field = self.get_by_placeholder(
            page_form, placeholder)
        field.send_keys(' ')
        field.send_keys(Keys.ENTER)

        page_form = self.get_form_by_xpath(
            '/html/body/main/div[2]/form/div[1]')

        self.assertIn(
            error, page_form.text)

    def test_password_mismatch_message(self):
        url = reverse('accounts:register')
        self.browser.get(f'{self.live_server_url}{url}')

        page_form = self.get_form_by_xpath(
            '/html/body/main/div[2]/form/div[1]')
        register_form = UserRegisterForm()

        password1 = self.get_by_placeholder(
            page_form, 'Type your password')
        password2 = self.get_by_placeholder(
            page_form, 'Repeat your password')
        self.get_by_placeholder(
            page_form, 'Your e-mail').send_keys('dummy@email.com')

        password1.send_keys('P4ssW0rdD4ta')
        password2.send_keys('P4ssW0rdD4ta22')
        self.fill_form_dummy_data(page_form)
        password2.send_keys(Keys.ENTER)

        page_form = self.get_form_by_xpath(
            '/html/body/main/div[2]/form/div[1]')

        self.assertIn('Both password fields must be equal', page_form.text)

    def test_user_valid_data_register_sucessfully(self):
        fields = [
            ('Ex.: John', 'First Name'),
            ('Ex.: Doe', 'Last Name'),
            ('Your e-mail', 'dummy@email.com'),
            ('Type your password', 'P4ssW0rd'),
            ('Repeat your password', 'P4ssW0rd'),
        ]

        url = reverse('accounts:register')
        self.browser.get(f'{self.live_server_url}{url}')

        page_form = self.get_form_by_xpath(
            '/html/body/main/div[2]/form/div[1]')

        for placeholder, data in fields:
            field = self.get_by_placeholder(page_form, placeholder)
            field.send_keys(data)

        actions = ActionChains(self.browser)
        actions.send_keys(Keys.ENTER).perform()

        self.assertIn(
            'You have been registered successfully! Now login in your account',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
