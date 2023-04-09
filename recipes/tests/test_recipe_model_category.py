from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes.models import Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category()
        return super().setUp()

    def test_category_model_max_length(self):
        self.category.name = 'A' * 65

        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category_string_representation_return_the_title(self):
        needed = 'String Representation'
        self.category.name = needed
        self.category.full_clean()
        self.category.save()

        self.assertEqual(str(self.category), needed)
