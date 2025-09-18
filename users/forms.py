from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
