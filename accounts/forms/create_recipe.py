from django import forms
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..validators import RecipeValidatorForm
from recipes.models import Recipe
from utils.functions import add_attr, add_placeholder


class CreateRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields["preparation_steps"], "class", "span-2")
        add_placeholder(self.fields["title"], _("Type here your title"))
        add_placeholder(
            self.fields["description"], _("Type here the description of the recipe")
        )
        add_placeholder(
            self.fields["preparation_time"], _("In minutes or hours, you choose!")
        )
        add_placeholder(self.fields["servings"], _("In people, portions or plates"))

    slug = forms.SlugField(
        help_text=(
            "If you don't want to set one, the slug is defined automatically if empty!"
        ),
        required=False,
    )

    class Meta:
        model = Recipe
        fields = (
            "title",
            "description",
            "slug",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "image",
        )

        widgets = {
            "servings_unit": forms.Select(
                choices=(
                    (_("People"), _("People")),
                    (_("Portions"), _("Portions")),
                    (_("Plates"), _("Plates")),
                ),
                attrs={"class": "span-2"},
            ),
            "preparation_time_unit": forms.Select(
                choices=((_("Minute(s)"), _("Minute(s)")), (_("Hour(s)"), _("Hour(s)")))
            ),
            "image": forms.FileInput(
                attrs={"class": "span-2"},
            ),
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        RecipeValidatorForm(data=cleaned_data, ErrorClass=ValidationError)
