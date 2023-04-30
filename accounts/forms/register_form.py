from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User
from utils import functions


class UserRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        functions.add_placeholder(self.fields['email'], 'Your e-mail')
        functions.add_placeholder(self.fields['first_name'], 'Ex.: John')
        functions.add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        functions.add_placeholder(
            self.fields['password'], 'Type your password')
        functions.add_placeholder(
            self.fields['password2'], 'Repeat your password')

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required', },
        label="E-mail",
        help_text="The e-mail must be valid",
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name, please',
                        'min_length': 'Your first name must have at least 3 characters',
                        'max_length': 'Your first name must have a maximum of 100 characters'},
        label="First name",
        help_text="Your first name must have at least 3 characters and a maximum of 100 characters",
        min_length=3, max_length=100,
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name, please',
                        'min_length': 'Your last name must have at least 3 characters',
                        'max_length': 'Your last name must have a maximum of 100 characters'},
        label="Last name",
        help_text="Your last name must have at least 3 characters and a maximum of 100 characters",
        min_length=3, max_length=100,
    )

    password = forms.CharField(
        error_messages={'required': 'The password must not be empty'},
        widget=forms.PasswordInput(),
        label='Password',
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[functions.strong_password],
    )

    password2 = forms.CharField(
        error_messages={'required': 'Please, repeat your password'},
        widget=forms.PasswordInput(),
        label='Confirmation of Password',
        help_text='Type your password again to confirm'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'email': 'E-mail',
            'first_name': 'First name',
            'last_name': 'Last name',
        }

    def clean(self):
        data = super().clean()

        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                "Both password fields must be equal", code='invalid')

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            }
            )
