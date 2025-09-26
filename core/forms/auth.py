from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    invited_by = forms.CharField(label="Ник пользователя, пригласившего на платформу", required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "invited_by"]
