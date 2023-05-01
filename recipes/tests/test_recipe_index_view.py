from django.urls import resolve, reverse
from unittest.mock import patch

from recipes import views
from .recipe_base import RecipeTestBase


class RecipeIndexViewTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe(author={'first_name': 'vinicius'})
        self.recipe.is_published = False
        self.recipe.save()

        return super().setUp()

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
        self.recipe.is_published = True
        self.recipe.save()

        response = self.client.get(reverse('recipes:index'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', response_content)
        self.assertIn('10 Minutos', response_content)
        self.assertIn('vinicius', response_content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_pagination_is_rendering_the_defined_value_of_recipes_per_page(self):
        self.make_recipe_in_batch(8)

        with patch('recipes.views.Index.paginate_by', new=3):
            url = reverse('recipes:index')
            response = self.client.get(url)

            response_context = response.context['paginator_func']
            self.assertEqual(response_context.get('total_pages'), 3)
