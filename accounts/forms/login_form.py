from django import forms
from django.utils.translation import gettext_lazy as _

from utils.functions import add_placeholder


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['email'], _('Type your e-mail'))
        add_placeholder(self.fields['password'], _('Type your password'))

    email = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('Password')
    )
