from django.urls import reverse

from .recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe(category={'name': 'Lanches'})
        self.recipe.save()

        self.recipe2 = self.make_recipe(
            category={'name': 'Receitas'}, author={'email': 'admin2@gmail.com'})
        self.recipe2.save()

        return super().setUp()

    def test_category_view_returns_code_200_0K(self):
        url = reverse('recipes:category', kwargs={'category_name': 'Lanches'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_category_view_just_render_recipes_from_the_specific_category(self):
        url = reverse('recipes:category', kwargs={'category_name': 'Lanches'})
        response = self.client.get(url)

        response_context = response.context['recipes']

        self.assertIn(self.recipe, response_context)
        self.assertNotIn(self.recipe2, response_context)
