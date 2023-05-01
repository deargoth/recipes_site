from .recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes.models import Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_without_default_fields(self):
        recipe = Recipe(
            title='Default Recipe Title',
            description='Default Recipe Description',
            slug='',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=4,
            servings_unit='Porções',
            preparation_steps='Default Recipe Preparation Steps',
            author=self.make_author(email='demodemo@email.com'),
            category=self.make_category(name='Hunts'),
        )

        recipe.full_clean()
        recipe.save()

        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 255),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_false_by_default(self):
        recipe = self.make_recipe_without_default_fields()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_without_default_fields()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation_of_model(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed)
