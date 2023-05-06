from django import forms

from recipes.models import Recipe
from utils.functions import add_attr, add_placeholder


class CreateRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
