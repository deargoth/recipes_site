from django.test import TestCase
from django.urls import reverse, resolve

from accounts import views
from accounts.models import User


class TestDashboardView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='demoadmin@gmail.com',
            password='demodemo'
        )

        return super().setUp()

    def test_dashboard_view_url_is_correct(self):
        url = reverse('accounts:dashboard')
        self.assertEqual(url, '/accounts/dashboard/')

    def test_dashboard_view_returns_code_200_OK(self):
        self.client.login(email='demoadmin@gmail.com', password='demodemo')

        url = reverse('accounts:dashboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_class_is_correct(self):
        url = reverse('accounts:dashboard')
        response = resolve(url)

        self.assertIs(response.func.view_class, views.Dashboard)

    def test_dashboard_view_render_correct_template(self):
        self.client.login(email='demoadmin@gmail.com', password='demodemo')

        url = reverse('accounts:dashboard')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'accounts/dashboard.html')

    def test_if_dashboard_view_returns_to_login_if_not_authenticated(self):
        url = reverse('accounts:dashboard')
        expected_url = reverse('accounts:login')
        response = self.client.get(url)

        self.assertRedirects(response, expected_url)
