import pytest

from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
from .recipe_functional_tests_base_class import RecipeBaseFunctionalTests
from recipes.tests.recipe_base import RecipeMixin


@pytest.mark.functional_test
class TestRecipeIndexPage(RecipeMixin, RecipeBaseFunctionalTests):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.make_recipe_in_batch(18)

        with patch('recipes.views.Index.paginate_by', new=3):
            self.browser.get(self.live_server_url)
            self.sleep()
            body = self.browser.find_element(By.TAG_NAME, 'body')
            self.assertNotIn('No recipes found here', body.text)

    def test_recipe_search_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(9)
        title_needed = "This is what I need"

        recipes[0].title = title_needed
        recipes[0].save()

        with patch('recipes.views.Index.paginate_by', new=3):
            # User opens our site
            self.browser.get(self.live_server_url)

            # See a search field with the placeholder "Search for a recipe"
            search_input = self.browser.find_element(
                By.XPATH,
                '//input[@placeholder="Search for a recipe"]'
            )

            # Click on the input and search for "This is what I need"
            # to encounter the recipe with this title
            search_input.send_keys(recipes[0].title)
            search_input.send_keys(Keys.ENTER)

            self.sleep()

            self.assertIn(
                title_needed,
                self.browser.find_element(
                    By.CLASS_NAME, 'main-content-list').text
            )

    def test_recipe_index_page_pagination(self):
        self.make_recipe_in_batch(9)

        with patch('recipes.views.Index.paginate_by', new=3):
            # User opens our site
            self.browser.get(self.live_server_url)

            # See the pagination and click on the page 2
            page2 = self.browser.find_element(
                By.XPATH,
                '//a[@aria-label="Go to page 2"]'
            )
            page2.click()

            # See that there are more 3 recipes on the second page
            self.assertEqual(
                len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
                3
            )

            self.sleep()
