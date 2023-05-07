from django import forms
from collections import defaultdict
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.functions import add_attr, add_placeholder


class CreateRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields['preparation_steps'], 'class', 'span-2')
        add_placeholder(self.fields['title'], 'Type here your title')
        add_placeholder(self.fields['description'],
                        'Type here the description of the recipe')
        add_placeholder(self.fields['preparation_time'],
                        'In minutes or hours, you choose!')
        add_placeholder(self.fields['servings'],
                        'In people, portions or plates')

    slug = forms.SlugField(
        help_text="If you don't want to set one, the slug is defined automatically if empty!",
        required=False,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ('preparation_steps_is_html',
                   'is_published', 'author', 'category',)

        widgets = {
            'servings_unit': forms.Select(
                choices=(
                    ('People', 'People'),
                    ('Portions', 'Portions'),
                    ('Plates', 'Plates')
                ),
                attrs={
                    'class': 'span-2'
                },
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas')
                )
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'span-2'
                },
            ),
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_steps = cleaned_data.get('preparation_steps')

        if title:
            if len(title) < 6:
                self._my_errors['title'].append(
                    'Title must have at least 6 characters.')

        if description:
            if len(description) < 10:
                self._my_errors['title'].append(
                    'Description must have at least 10 characters.')

        if preparation_steps:
            if len(preparation_steps) < 20:
                self._my_errors['title'].append(
                    'The preparation steps must have at least 20 characters.')

        if title and description:
            if title == description:
                self._my_errors['title'].append(
                    'The title cannot be equal to description')
                self._my_errors['description'].append(
                    'The description cannot be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)
