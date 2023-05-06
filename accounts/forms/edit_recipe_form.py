from django import forms

from recipes.models import Recipe
from utils.functions import add_attr


class EditRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['preparation_steps'], 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ('author', 'is_published',
                   'preparation_steps_is_html', 'category')
        widgets = {
            'servings_unit': forms.Select(
                attrs={
                    'class': 'span-2'
                },
                choices=(
                    ('Porções', 'Porções'),
                    ('Pessoas', 'Pessoas'),
                    ('Pedaços', 'Pedaços'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
        }
