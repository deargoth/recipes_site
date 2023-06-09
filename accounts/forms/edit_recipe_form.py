from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from collections import defaultdict

from recipes.models import Recipe
from utils.functions import add_attr


class EditRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields['preparation_steps'], 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ('author', 'is_published',
                   'preparation_steps_is_html', 'category', 'tags')
        widgets = {
            'servings_unit': forms.Select(
                attrs={
                    'class': 'span-2'
                },
                choices=(
                    (_('Portions'), _('Portions')),
                    (_('People'), _('People')),
                    (_('Pieces'), _('Pieces')),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    (_('Minutes'), _('Minutes')),
                    (_('Hours'), _('Hours')),
                )
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
        }

    def clean(self):
        super_clean = super().clean()

        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_steps = cleaned_data.get('preparation_steps')

        if len(title) < 6:
            self._my_errors['title'].append(
                _('Title must have at least 6 characters.'))

        if len(description) < 10:
            self._my_errors['title'].append(
                _('Description must have at least 10 characters.'))

        if title == description:
            self._my_errors['title'].append(
                _('The title cannot be equal to description'))
            self._my_errors['description'].append(
                _('The description cannot be equal to title'))

        if len(preparation_steps) < 20:
            self._my_errors['title'].append(
                _('The preparation steps must have at least 20 characters.'))

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
