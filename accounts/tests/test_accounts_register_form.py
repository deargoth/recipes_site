from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from accounts.forms import UserRegisterForm


class UserRegisterFormUnitTests(TestCase):
    @parameterized.expand([
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_register_form_placeholders_are_correct(self, field, placeholder):
        form = UserRegisterForm()
        field_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, field_placeholder)

    @parameterized.expand([
        ('email', 'The e-mail must be valid'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),
        ('password2', 'Type your password again to confirm'),
        ('first_name', 'Your first name must have at least 3 characters and a maximum of 100 characters'),
        ('last_name', 'Your last name must have at least 3 characters and a maximum of 100 characters'),
    ])
    def test_register_form_help_texts_are_correct(self, field, help_text):
        form = UserRegisterForm()
        current_help_text = form[field].field.help_text

        self.assertEqual(help_text, current_help_text)

    @parameterized.expand([
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Confirmation of Password'),
    ])
    def test_register_form_labels_are_correct(self, field, label):
        form = UserRegisterForm()
        current_label = form[field].field.label

        self.assertEqual(label, current_label)


class UserRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'email': 'email@anyemail.com',
            'first_name': 'first',
            'last_name': 'last',
            'password': 'Str0ngP@ss',
            'password2': 'Str0ngP@ss',
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('email', 'E-mail is required'),
        ('first_name', 'Write your first name, please'),
        ('last_name', 'Write your last name, please'),
        ('password', 'The password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_register_form_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('accounts:register')

        response = self.client.post(url, self.form_data)
        response_context = response.context['register_form'].errors.get(field)

        self.assertIn(msg, response_context)

    @parameterized.expand([
        ('first_name', 'Your first name must have at least 3 characters', 3),
        ('last_name', 'Your last name must have at least 3 characters', 3)
    ])
    def test_register_form_min_length_of_fields(self, field, error_msg, min_length):
        self.form_data[field] = 'a' * (min_length - 1)
        url = reverse('accounts:register')

        response = self.client.post(url, self.form_data)
        response_context = response.context['register_form'].errors.get(
            field)

        self.assertIn(error_msg, response_context)

    @parameterized.expand([
        ('first_name', 'Your first name must have a maximum of 100 characters', 100),
        ('last_name', 'Your last name must have a maximum of 100 characters', 100)
    ])
    def test_register_form_max_length_of_fields(self, field, error_msg, max_length):
        self.form_data[field] = 'a' * (max_length + 1)
        url = reverse('accounts:register')

        response = self.client.post(url, self.form_data)
        response_context = response.context['register_form'].errors.get(
            field)

        self.assertIn(error_msg, response_context)

    def test_register_form_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'StrongPass'

        url = reverse("accounts:register")
        response = self.client.post(url, self.form_data)

        response_context = response.context['register_form'].errors.get(
            'password')
        error_expected = 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'

        self.assertIn(error_expected, response_context)

    def test_register_form_password_fields_are_equal(self):
        self.form_data['password'] = 'Str0ngPass'
        self.form_data['password2'] = 'Str0ngPass2'

        url = reverse("accounts:register")
        response = self.client.post(url, self.form_data)

        response_context = response.context['register_form'].errors.get(
            'password')
        error_expected = 'Both password fields must be equal'

        self.assertIn(error_expected, response_context)
