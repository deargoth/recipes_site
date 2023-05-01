from django.test import TestCase
from django.urls import reverse

from accounts import forms
from accounts.models import User


class TestRegisterView(TestCase):
    def setUp(self):
        self.form_data = {
            'email': 'formtest@gmail.com',
            'first_name': 'test',
            'last_name': 'register',
            'password': 'Str0ngP4ss',
            'password2': 'Str0ngP4ss',
        }

        self.user = User.objects.create_user(
            email='registertest@gmail.com',
        )
        self.user.set_password('123456')
        self.user.save()

        return super().setUp()

    def test_register_view_is_rendering_correct_template(self):
        url = reverse("accounts:register")
        self.assertEqual(url, '/accounts/register/')

    def test_register_view_is_returning_code_200_OK(self):
        url = reverse("accounts:register")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_register_view_is_loading_correct_form_to_register(self):
        url = reverse("accounts:register")
        response = self.client.get(url)

        response_context = response.context['register_form']
        self.assertIs(response_context.__class__, forms.UserRegisterForm)

    def test_register_view_is_redirecting_to_home_if_already_authenticated(self):
        self.client.login(
            email='registertest@gmail.com',
            password='123456'
        )

        url = reverse("accounts:register")
        expected_url = reverse("recipes:index")
        response = self.client.get(url)

        self.assertRedirects(response, expected_url)

    def test_register_view_redirect_to_login_if_register_is_complete(self):
        url = reverse('accounts:register')
        expected_url = reverse('accounts:login')

        response = self.client.post(url, self.form_data)

        self.assertRedirects(response, expected_url)
