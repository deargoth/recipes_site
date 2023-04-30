from django.test import TestCase
from django.urls import reverse, resolve


from accounts.models import User
from accounts import views


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='logintest@email.com',
        )
        self.user.set_password('123456')
        self.user.save()

        return super().setUp()

    def test_login_page_url_is_correct(self):
        url = reverse('accounts:login')
        self.assertEqual(url, '/accounts/login/')

    def test_login_page_is_returning_code_200_OK(self):
        url = reverse('accounts:login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_login_page_is_rendering_correct_template_view(self):
        url = reverse('accounts:login')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_page_is_rendering_correct_view_class(self):
        response = resolve(reverse('accounts:login'))

        self.assertIs(response.func.view_class, views.Login)

    def test_login_page_is_redirecting_to_index_if_user_already_logged(self):
        self.client.login(
            email='logintest@email.com',
            password='123456',
        )

        url = reverse('accounts:login')
        response = self.client.get(url)

        expected_url = reverse('recipes:index')
        self.assertRedirects(response, expected_url)
