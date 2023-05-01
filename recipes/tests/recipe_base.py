from django.test import TestCase
from recipes.models import Recipe, Category
from accounts.models import User


class RecipeMixin:
    def make_recipe(
        self,
        author=None,
        category=None,
        title='Recipe Title',
        description='Description Recipe',
        slug='',
        preparation_time='10',
        preparation_time_unit='Minutos',
        servings='5',
        servings_unit='Porções',
        preparation_steps='Recipe PreparatioN Setps',
        preparation_steps_is_html=False,
        is_published=True,
    ):

        if author is None:
            author = {}

        if category is None:
            category = {}

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            author=self.make_author(**author),
            category=self.make_category(**category),
        )

    def make_category(self, name='Category'):
        return Category.objects.create(
            name=name
        )

    def make_author(
        self,
        email='admin@email.com',
        password='demodemo',
        first_name='Admin',
        last_name='Admin'
    ):
        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

    def make_recipe_in_batch(self, quantity=9):
        recipes = []

        for i in range(quantity):
            kwargs = {'title': f'Recipe of number {i}',
                      'author': {'email': f'email{i}@gmail.com'}}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(RecipeMixin, TestCase):
    def setUp(self):
        return super().setUp()
