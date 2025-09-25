from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
