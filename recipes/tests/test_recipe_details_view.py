from django.urls import reverse

from .test_recipe_base import RecipeTestBase


class RecipeDetailsViewTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe(author={'first_name': 'vinicius'})
        self.recipe.save()

        return super().setUp()

    def test_details_view_is_returning_code_200_OK(self):
        url = reverse('recipes:details', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_details_view_is_redirecting_to_index_if_recipe_isnt_published(self):
        self.recipe.is_published = False
        self.recipe.save()

        url = reverse('recipes:details', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)

        expected_url = reverse('recipes:index')
        self.assertRedirects(response, expected_url)
