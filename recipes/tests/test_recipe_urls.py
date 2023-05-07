from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_index_url_is_correct(self):
        url = reverse('recipes:index')
        self.assertEqual(url, '/')

    def test_recipe_details_url_is_correct(self):
        url = reverse('recipes:details', kwargs={'pk': 1})
        self.assertEqual(url, '/recipes/details/1')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_name': 'Lanches'})
        self.assertEqual(url, '/recipes/Lanches')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
