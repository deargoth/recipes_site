from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from recipes.tests.recipe_base import RecipeTestBase


class TestEditRecipeView(RecipeTestBase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            email='admin@gmail.com',
            password='demodemo'
        )

        self.recipe = self.make_recipe()
        return super().setUp()

    def test_edit_recipe_view_url_is_correct(self):
        url = reverse('accounts:edit_recipe', kwargs={'pk': self.recipe.pk})
        self.assertEqual(
            url, f'/accounts/dashboard/editrecipe/{self.recipe.pk}')

    def test_edit_recipe_template_view(self):
        self.client.login(email='admin@gmail.com', password='demodemo')

        url = reverse('accounts:edit_recipe', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'accounts/edit_recipe.html')

    def test_edit_recipe_status_code(self):
        self.client.login(email='admin@gmail.com', password='demodemo')

        url = reverse('accounts:edit_recipe', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_recipe_just_accept_authenticated_users(self):
        url = reverse('accounts:edit_recipe', kwargs={'pk': self.recipe.pk})
        expected_url = reverse('accounts:login')
        response = self.client.get(url)

        self.assertRedirects(response, expected_url)
