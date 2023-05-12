from django import forms
from django.contrib.auth import get_user_model

from utils.functions import add_attr
from accounts.models import Profile

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        error_messages={'invalid': 'The first name must not be empty'}
    )

    last_name = forms.CharField(
        error_messages={'invalid': 'This last name must not be empty'}
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['biography'], 'class', 'span-2')

    class Meta:
        model = Profile
        fields = ('biography', 'slug', 'image')
        widgets = {
            'image': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            )
        }
