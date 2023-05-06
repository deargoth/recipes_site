from django import forms

from recipes.models import Recipe
from utils.functions import add_attr


class EditRecipeForm(forms.ModelForm):

    preparation_time_unit = forms.CharField(
        error_messages={'required': 'This field cannot be empty'},
        help_text='Ex.: Hours, minutes, days',
    )
    servings_unit = forms.CharField(
        error_messages={'required': 'This field cannot be empty'},
        help_text='Ex.: People, person',
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ('author', 'is_published',
                   'preparation_steps_is_html', 'category')
