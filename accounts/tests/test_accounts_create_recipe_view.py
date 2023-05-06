from django.test import TestCase
from django.urls import reverse, resolve

from accounts import views
from accounts.models import User


class TestCreateRecipeView(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user(
            email='admin@gmail.com',
            password='demodemo'
        )
        return super().setUp(*args, **kwargs)

    def test_create_recipe_url_is_correct(self):
        url = reverse('accounts:create_recipe')
        self.assertEqual(url, '/accounts/dashboard/recipe/create/')

    def test_create_recipe_redirects_user_to_login_if_not_authenticated(self):
        url = reverse('accounts:create_recipe')
        expected_url = reverse('accounts:login')

        response = self.client.get(url)

        self.assertRedirects(response, expected_url)

    def test_create_recipe_status_code_is_200_OK(self):
        self.client.login(email='admin@gmail.com', password='demodemo')

        url = reverse('accounts:create_recipe')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_recipe_template_used_is_correct(self):
        self.client.login(email='admin@gmail.com', password='demodemo')

        url = reverse('accounts:create_recipe')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'accounts/create_recipe.html')

    def test_create_recipe_view_class_is_correct(self):
        self.client.login(email='admin@gmail.com', password='demodemo')

        url = reverse('accounts:create_recipe')
        response = resolve(url)

        self.assertIs(response.func.view_class, views.CreateRecipe)
