from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import UserCreationForm


# class RegisterAuthor(forms.ModelForm):
#     email = forms.EmailField(
#         label='E-mail',
#         error_messages={'required': 'E-mail is required'},
#         help_text='The e-mail must be valid',
#     )

#     first_name = forms.CharField(
#         label='First name',
#         error_messages={'required': 'Your name cannot be empty'}
#     )

#     last_name = forms.CharField(
#         label='Last name',
#         error_messages={'required': 'Your name cannot be empty'},
#     )

#     password = forms.CharField(
#         widget=forms.PasswordInput(),
#         label='Password',
#         error_messages={
#             'required': 'Password must not be empty'
#         },
#         help_text='Password must have at least one uppercase letter, \
#         one lowercase letter and one number. The length should be at least 8 characters.',
#         validators=[strong_password]
#     )

#     password2 = forms.CharField(
#         widget=forms.PasswordInput(),
#         label="Confirm your password",
#         help_text='Please, confirm your password',
#         error_messages={'required': 'You need to confirm your password'},
#     )

#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name', 'password', 'password2')

#     def clean(self):
#         data = super().clean()

#         email = data.get('email')
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         password = data.get('password')
#         password2 = data.get('password2')

#         email_db = User.objects.filter(email=email)

#         if email_db.exists():
#             raise ValidationError(
#                 'This e-mail is already in use',
#                 code='invalid'
#             )

#         if len(first_name) < 3:
#             self.add_error('first_name',
#                            'Your name needs to have at least 3 letters')

#         if len(last_name) < 3:
#             self.add_error('last_name',
#                            'Your last name needs to have at least 3 letters')

#         if password != password2:
#             password_confirmation_error = ValidationError(
#                 "The both password's must be equal",
#                 code='invalid'
#             )
#             raise ValidationError({
#                 'password': password_confirmation_error,
#                 'password2': [
#                     password_confirmation_error,
#                 ]
#             })


class RegisterAuthor(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', ]


class LoginAuthor(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
