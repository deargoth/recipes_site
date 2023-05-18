from django import forms
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RecipeValidatorForm:
    def __init__(self, data, ErrorClass, errors=None):
        super().__init__()
        self.errors = defaultdict(list) if errors == None else errors
        self.ErrorClass = ValidationError if ErrorClass == None else ErrorClass
        self.data = data
        self.clean()

    def clean(self):
        self.clean_title()
        self.clean_description()
        self.clean_preparation_steps()

        data = self.data

        title = data.get("title")
        description = data.get("description")

        if title and description:
            if title == description:
                self.errors["title"].append(
                    _("The title cannot be equal to description")
                )
                self.errors["description"].append(
                    _("The description cannot be equal to title")
                )

        if self.errors:
            raise ValidationError(self.errors)

    def clean_title(self):
        title = self.data.get("title")

        if title:
            if len(title) < 6:
                self.errors["title"].append(_("Title must have at least 6 characters."))

        return title

    def clean_description(self):
        description = self.data.get("description")

        if description:
            if len(description) < 6:
                self.errors["description"].append(
                    _("Description must have at least 6 characters.")
                )

        return description

    def clean_preparation_steps(self):
        preparation_steps = self.data.get("preparation_steps")

        if preparation_steps:
            if len(preparation_steps) < 20:
                self.errors["title"].append(
                    _("The preparation steps must have at least 20 characters.")
                )
