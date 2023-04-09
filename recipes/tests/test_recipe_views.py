from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.models import User, Category, Recipe
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_index_view_is_correct(self):
        view = resolve(reverse('recipes:index'))
        self.assertIs(view.func.view_class, views.Index)

    def test_recipe_index_view_return_code_200_OK(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_index_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertTemplateUsed(response, 'recipes/pages/index.html')

    def test_recipe_index_returns_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertIn(
            '<h1>No recipes found here 😢</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_index_loads_recipes(self):
        self.make_recipe(author={'first_name': 'vinicius'})
        response = self.client.get(reverse('recipes:index'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', response_content)
        self.assertIn('10 Minutos', response_content)
        self.assertIn('vinicius', response_content)
        self.assertEqual(len(response_context_recipes), 1)
